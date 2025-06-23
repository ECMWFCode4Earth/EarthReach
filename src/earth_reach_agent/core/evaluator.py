import re
from dataclasses import MISSING, dataclass, fields
from io import BytesIO
from typing import Any, List, Union, get_args, get_origin

import earthkit.plots as ekp
from PIL import Image
from PIL.ImageFile import ImageFile

from earth_reach_agent.core.generator import FigureMetadata
from earth_reach_agent.core.llm import BaseLLM, create_llm
from earth_reach_agent.core.prompts import get_default_criteria_evaluator_user_prompt


@dataclass
class CriteriaEvaluatorOutput:
    criteria: str
    score: int
    reasoning: str | None = None

    def is_score_valid(self) -> bool:
        """
        Check if the score is within a valid range (0 to 5).

        Returns:
            bool: True if the score is valid, False otherwise.
        """
        return 0 <= self.score <= 5

    def __post_init__(self):
        if not self.is_score_valid():
            raise ValueError("Score must be between 0 and 5.")


class CriteriaEvaluator:
    """Evaluator class for evaluating the quality of text based on a specified criteria."""

    def __init__(
        self, llm: BaseLLM, system_prompt: str | None, user_prompt: str
    ) -> None:
        self.llm = llm
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

    def evaluate(
        self,
        description: str,
        figure: ekp.Figure | None = None,
        image: ImageFile | None = None,
    ) -> CriteriaEvaluatorOutput:
        if figure is not None and image is not None:
            raise ValueError(
                "Only one of 'figure' or 'image' can be provided, not both."
            )
        if figure is not None:
            # TODO(medium): If metadata extraction failes, continue without it
            metadata = self._get_metadata_from_figure(figure)
            self.user_prompt = self._update_user_prompt_with_metadata(
                self.user_prompt, metadata
            )
            image = self._get_image_from_figure(figure)
        elif image is None and figure is None:
            raise ValueError(
                "Either 'figure' or 'image' must be provided to generate a description."
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

    def parse_llm_response(self, response: str) -> CriteriaEvaluatorOutput:
        """
        Parse the XML-tagged response from the CriteriaEvaluator Agent into structured data.

        Args:
            response (str): The full llm response string containing XML tags

        Returns:
            CriteriaEvaluatorOutput: Parsed evaluation content

        Raises:
            ValueError: If the response string is empty or None, or if required fields are missing
            Exception: If a parsing error occurs for any field
        """
        if not response or not response.strip():
            raise ValueError("Response string is empty or None")

        dataclass_fields = fields(CriteriaEvaluatorOutput)

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
                            content, field_name, field_type
                        )
                        extracted_values[field_name] = converted_value
            except Exception as e:
                parsing_errors.append(f"Failed to parse field '{field_name}': {str(e)}")

        required_fields = [
            f.name
            for f in dataclass_fields
            if f.default == MISSING and f.default_factory == MISSING
        ]

        missing_required = [f for f in required_fields if f not in extracted_values]
        if missing_required:
            raise ValueError(
                f"Missing required fields in XML response: {missing_required}"
            )

        if parsing_errors:
            raise Exception(f"Parsing errors occurred: {'; '.join(parsing_errors)}")

        try:
            return CriteriaEvaluatorOutput(**extracted_values)
        except Exception as e:
            raise Exception(
                f"Failed to create CriteriaEvaluatorOutput instance: {str(e)}"
            )

    def convert_to_field_type(
        self, content: str, field_name: str, field_type: Any
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
            except ValueError:
                raise ValueError(
                    f"Cannot convert '{content}' to integer for field '{field_name}'"
                )

        elif field_type is float:
            try:
                return float(content)
            except ValueError:
                raise ValueError(
                    f"Cannot convert '{content}' to float for field '{field_name}'"
                )

        elif field_type is bool:
            lower_content = content.lower().strip()
            if lower_content in ("true", "1", "yes", "on", "y"):
                return True
            elif lower_content in ("false", "0", "no", "off", "n"):
                return False
            else:
                raise ValueError(
                    f"Cannot convert '{content}' to boolean for field '{field_name}'. "
                    f"Expected: true/false, 1/0, yes/no, on/off, y/n"
                )

        elif field_type is str:
            return content

        else:
            if hasattr(field_type, "__call__"):
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
        self, user_prompt: str, metadata: FigureMetadata
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
                    "description", "No description available"
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


class EvaluatorCriteriaFactory:
    """Factory class for creating single criteria evaluator agents."""

    @staticmethod
    def create(criterion: str, llm: BaseLLM | None = None) -> CriteriaEvaluator:
        """
        Create a CriteriaEvaluator instance based on the provided criteria.

        Args:
            criteria (str): Criteria name to create evaluators for.
            llm (BaseLLM | None): Optional LLM instance to use for evaluation.

        Returns:
            CriteriaEvaluator: CriteriaEvaluator instance.
        """
        if criterion not in ["coherence", "fluency", "consistency", "relevance"]:
            raise ValueError(f"Unsupported criteria: {criterion}")

        if not llm:
            llm = create_llm()

        user_prompt = get_default_criteria_evaluator_user_prompt(criterion)

        return CriteriaEvaluator(llm=llm, system_prompt=None, user_prompt=user_prompt)


class EvaluatorAgent:
    """Agent class for evaluating the quality of weather chart descriptions."""

    def __init__(self, criteria: List[str]) -> None:
        """
        Initialize the EvaluatorAgent.

        Args:
            parameters, quality criteria, etc..
        """
        pass

    def evaluate(self, text: str, criteria: dict):
        pass

    def is_text_length_lesser_than_max(self, text: str, max_length: int = 1000) -> bool:
        """
        Check if the length of the text is lesser than the specified maximum length.

        Args:
            text (str): The text to check.
            max_length (int): The maximum length of the text.

        Returns:
            bool: True if the text length is valid, False otherwise.
        """
        return len(text) <= max_length

    def is_text_length_greater_than_min(self, text: str, min_length: int = 100) -> bool:
        """
        Check if the length of the text is greater than the specified minimum length.

        Args:
            text (str): The text to check.
            min_length (int): The minimum length of the text.

        Returns:
            bool: True if the text length is more than the minimum, False otherwise.
        """
        return min_length <= len(text)
