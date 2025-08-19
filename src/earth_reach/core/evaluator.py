"""
Evaluator Agent module.

This module provides the main structure and classes for evaluating weather chart descriptions
automatically against a set of quality criteria.
"""

import re

from dataclasses import MISSING, dataclass, fields
from io import BytesIO
from typing import Any, Union, get_args, get_origin

import earthkit.plots as ekp

from PIL import Image
from PIL.ImageFile import ImageFile

from earth_reach.config.logging import get_logger
from earth_reach.core.generator import FigureMetadata
from earth_reach.core.llm import LLMInterface, create_llm
from earth_reach.core.prompts.evaluator import (
    get_default_criterion_evaluator_user_prompt,
)

logger = get_logger(__name__)


@dataclass
class CriterionEvaluatorOutput:
    """Structured representation of the criterion evaluator's output.

    Attributes:
        criterion: The criterion against which the text was evaluated.
        score: The score assigned to the text based on the criterion (0 to 5).
        reasoning: Optional reasoning for the score, if provided by the LLM.
    """

    name: str
    score: int
    reasoning: str | None = None

    def is_score_valid(self) -> bool:
        """
        Check if the score is within a valid range (0 to 5).

        Returns:
            bool: True if the score is valid, False otherwise.
        """
        return 0 <= self.score <= 5

    def __post_init__(self) -> None:
        if not self.is_score_valid():
            raise ValueError("Score must be between 0 and 5.")


class CriterionEvaluator:
    """Evaluator class for evaluating the quality of weather descriptions based on a specified criterion."""

    def __init__(
        self,
        criterion: str,
        llm: LLMInterface,
        system_prompt: str | None,
        user_prompt: str,
    ) -> None:
        if criterion not in ["coherence", "fluency", "consistency", "relevance"]:
            raise ValueError(f"Unsupported criterion: {criterion}")

        self.criterion = criterion
        self.llm = llm
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

    def evaluate(
        self,
        description: str,
        figure: ekp.Figure | None = None,
        image: ImageFile | None = None,
    ) -> CriterionEvaluatorOutput:
        if figure is not None and image is not None:
            raise ValueError(
                "Only one of 'figure' or 'image' can be provided, not both.",
            )
        if figure is not None:
            # TODO(medium): If metadata extraction fails, continue without it
            metadata = self._get_metadata_from_figure(figure)
            self.user_prompt = self._update_user_prompt_with_metadata(
                self.user_prompt,
                metadata,
            )
            image = self._get_image_from_figure(figure)
        elif image is None and figure is None:
            raise ValueError(
                "Either 'figure' or 'image' must be provided to generate a description.",
            )
        try:
            user_prompt = (
                self.user_prompt
                + f"\n\n# Description to evaluate\n\n{description}"
                + "\n\nPlease provide your evaluation of the description against the criteria."
            )
            response = self.llm.generate(
                user_prompt=user_prompt,
                system_prompt=self.system_prompt,
            )
            return self.parse_llm_response(response)
        except Exception as e:
            raise RuntimeError(f"Failed to generate response: {e}") from e

    def parse_llm_response(self, response: str) -> CriterionEvaluatorOutput:
        """
        Parse the XML-tagged response from the CriterionEvaluator Agent into structured data.

        Args:
            response (str): The full llm response string containing XML tags

        Returns:
            CriterionEvaluatorOutput: Parsed evaluation content

        Raises:
            ValueError: If the response string is empty or None, or if required fields are missing
            Exception: If a parsing error occurs for any field
        """
        if not response or not response.strip():
            raise ValueError("Response string is empty or None")

        dataclass_fields = fields(CriterionEvaluatorOutput)

        extracted_values = {}
        parsing_errors = []

        for field in dataclass_fields:
            field_name = field.name
            field_type = field.type

            pattern = rf"<{field_name}>(.*?)</{field_name}>"

            try:
                match = re.search(pattern, response, re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    if content:
                        converted_value = self.convert_to_field_type(
                            content,
                            field_name,
                            field_type,
                        )
                        extracted_values[field_name] = converted_value
            except Exception as e:
                parsing_errors.append(f"Failed to parse field '{field_name}': {e!s}")

        logger.warning(
            f"Parsing errors encountered: {parsing_errors}",
        ) if parsing_errors else None

        required_fields = [
            f.name
            for f in dataclass_fields
            if f.default == MISSING
            and f.default_factory == MISSING
            and f.name
            != "name"  # 'name' not required since it's set by object attribute
        ]

        missing_required = [f for f in required_fields if f not in extracted_values]
        if missing_required:
            raise ValueError(
                f"Missing required fields in XML response: {missing_required}",
            )

        try:
            return CriterionEvaluatorOutput(name=self.criterion, **extracted_values)
        except Exception as e:
            raise Exception(
                f"Failed to create CriterionEvaluatorOutput instance: {e!s}",
            ) from e

    def convert_to_field_type(
        self,
        content: str,
        field_name: str,
        field_type: Any,
    ) -> Any:
        """
        Convert string content to the appropriate type based on field type annotation.

        Args:
            content (str): The extracted string content
            field_name (str): Name of the field (for error reporting)
            field_type: The type annotation of the field

        Returns:
            The converted value with the correct type

        Raises:
            ValueError: If type conversion fails
        """
        origin = get_origin(field_type)

        if origin is Union:
            args = get_args(field_type)
            non_none_types = [arg for arg in args if arg is not type(None)]
            if non_none_types:
                field_type = non_none_types[0]
            else:
                return content

        if field_type is int:
            try:
                return int(content)
            except ValueError as e:
                raise ValueError(
                    f"Cannot convert '{content}' to integer for field '{field_name}'",
                ) from e

        elif field_type is float:
            try:
                return float(content)
            except ValueError as e:
                raise ValueError(
                    f"Cannot convert '{content}' to float for field '{field_name}'",
                ) from e

        elif field_type is bool:
            lower_content = content.lower().strip()
            if lower_content in ("true", "1", "yes", "on", "y"):
                return True
            if lower_content in ("false", "0", "no", "off", "n"):
                return False
            raise ValueError(
                f"Cannot convert '{content}' to boolean for field '{field_name}'. "
                f"Expected: true/false, 1/0, yes/no, on/off, y/n",
            )

        elif field_type is str:
            return content

        else:
            if callable(field_type):
                try:
                    return field_type(content)
                except Exception:
                    return content
            else:
                return content

    def _get_metadata_from_figure(self, figure: ekp.Figure) -> FigureMetadata:
        """
        Extract metadata from the given figure.

        Args:
            figure (ekp.Figure): The figure to extract metadata from.

        Returns:
            FigureMetadata: An object containing the extracted metadata.
        """
        metadata = FigureMetadata()

        plt_fig = figure.fig
        if plt_fig is None:
            raise ValueError("Matplotlib figure is None, cannot extract metadata.")

        axes = plt_fig.get_axes()

        metadata.title = axes[0].get_title()
        metadata.xlabel = axes[0].get_xlabel()
        metadata.ylabel = axes[0].get_ylabel()
        metadata.domain = figure._domain
        return metadata

    def _update_user_prompt_with_metadata(
        self,
        user_prompt: str,
        metadata: FigureMetadata,
    ) -> str:
        """
        Update the user prompt with metadata extracted from the figure.

        Args:
            user_prompt (str): The original user prompt.
            metadata (FigureMetadata): The metadata to include in the prompt.

        Returns:
            str: The updated user prompt with metadata included.
        """
        metadata_items = []
        for field_info in fields(metadata):
            value = getattr(metadata, field_info.name)
            if value is not None:
                description = field_info.metadata.get(
                    "description",
                    "No description available",
                )
                metadata_items.append(f"- {field_info.name} ({description}): {value}")

        if not metadata_items:
            return user_prompt

        metadata_str = "# FIGURE METADATA\n\n"
        metadata_str += "The following metadata was extracted from the figure:\n\n"
        metadata_str += "\n".join(metadata_items)

        return f"{user_prompt}\n\n{metadata_str}"

    def _get_image_from_figure(self, figure: ekp.Figure) -> ImageFile:
        """
        Convert the given figure to an image file.

        Args:
            figure (ekp.Figure): The figure to convert.

        Returns:
            ImageFile: The converted image file.
        """
        buffer = BytesIO()
        figure.save(buffer, format="png")
        buffer.seek(0)
        return Image.open(buffer)

    def append_user_prompt(self, text: str) -> None:
        """Append additional text to the user prompt."""
        self.user_prompt += f"\n\n{text.strip()}"


class CriterionEvaluatorFactory:
    """Factory class for creating single criterion evaluator agents."""

    @staticmethod
    def create(criterion: str, llm: LLMInterface | None = None) -> CriterionEvaluator:
        """
        Create a CriterionEvaluator instance based on the provided criterion.

        Args:
            criterion (str): Criterion name to create evaluators for.
            llm (LLMInterface | None): Optional LLM instance to use for evaluation.

        Returns:
            CriterionEvaluator: CriterionEvaluator instance.
        """
        if criterion not in ["coherence", "fluency", "consistency", "relevance"]:
            raise ValueError(f"Unsupported criterion: {criterion}")

        if not llm:
            llm = create_llm()

        user_prompt = get_default_criterion_evaluator_user_prompt(criterion)

        return CriterionEvaluator(
            criterion=criterion,
            llm=llm,
            system_prompt=None,
            user_prompt=user_prompt,
        )


class EvaluatorAgent:
    """Agent class for evaluating the quality of weather chart descriptions."""

    def __init__(self, criteria: list[str], llm: LLMInterface | None = None) -> None:
        """
        Initialize the EvaluatorAgent.

        Args:
            criteria (List[str]): List of criteria to evaluate against.
                Supported criteria: "coherence", "fluency", "consistency", "relevance".
            llm (LLMInterface | None): Optional LLM instance to use for evaluation.

        Raises:
            ValueError: If an unsupported criterion is provided.
            RuntimeError: If the evaluator creation fails.
        """
        for criterion in criteria:
            if criterion not in ["coherence", "fluency", "consistency", "relevance"]:
                raise ValueError(f"Unsupported criterion: {criterion}")

        self.criteria = criteria

        try:
            self.evaluators = [
                CriterionEvaluatorFactory.create(criterion, llm=llm)
                for criterion in criteria
            ]
        except Exception as e:
            raise RuntimeError(
                f"Failed to create evaluators for criteria {criteria}: {e}",
            ) from e

    def evaluate(
        self,
        description: str,
        figure: ekp.Figure | None = None,
        image: ImageFile | None = None,
    ) -> list[CriterionEvaluatorOutput]:
        """
        Evaluate the given text against the specified criteria.

        Args:
            text (str): The text to evaluate.

        Returns:
            List[CriterionEvaluatorOutput]: A list of evaluation results for each criterion.
        """
        if figure is not None and image is not None:
            raise ValueError(
                "Only one of 'figure' or 'image' can be provided, not both.",
            )

        try:
            evaluations = []
            for evaluator in self.evaluators:
                result = evaluator.evaluate(
                    description=description,
                    figure=figure,
                    image=image,
                )
                evaluations.append(result)

            return evaluations
        except Exception as e:
            raise RuntimeError(f"Failed to evaluate description: {e}") from e

    def append_user_prompt(self, text: str) -> None:
        """Append additional text to the user prompt of each criterion evaluator."""
        for evaluator in self.evaluators:
            evaluator.user_prompt += f"\n\n{text.strip()}"
