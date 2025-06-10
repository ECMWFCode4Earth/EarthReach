import re
from dataclasses import dataclass, field, fields
from io import BytesIO
from typing import List

import earthkit.plots as ekp
from PIL import Image
from PIL.ImageFile import ImageFile

from earth_reach_agent.core.llm import BaseLLM


@dataclass
class FigureMetadata:
    """Metadata extracted from a figure."""

    title: str | None = field(
        default=None, metadata={"description": "Figure title or heading"}
    )
    xlabel: str | None = field(
        default=None,
        metadata={"description": "X-axis label describing the horizontal dimension"},
    )
    ylabel: str | None = field(
        default=None,
        metadata={"description": "Y-axis label describing the vertical dimension"},
    )
    domain: str | None = field(
        default=None, metadata={"description": "Geographic domain of the figure"}
    )
    variables: List[str] | None = field(
        default=None,
        metadata={"description": "Key variables shown in the figure"},
    )


@dataclass
class GeneratorOutput:
    """
    Structured representation of the generator agent's output.

    Attributes:
        step_1: Data extraction and analysis content
        step_2: Pattern recognition and spatial analysis content
        step_3: Description planning and structure design content
        step_4: Description writing with verification content
        final_description: The final consolidated weather description
    """

    step_1: str | None = None
    step_2: str | None = None
    step_3: str | None = None
    step_4: str | None = None
    final_description: str | None = None

    def is_complete(self) -> bool:
        """
        Check if all required fields were successfully parsed.

        Returns:
            bool: True if all fields contain content, False otherwise
        """
        return all(
            getattr(self, field.name) is not None and getattr(self, field.name).strip()
            for field in fields(self)
        )

    def get_missing_fields(self) -> List[str]:
        """
        Return list of field names that were not successfully parsed.

        Returns:
            List[str]: Names of fields that are None or empty
        """
        return [
            field.name
            for field in fields(self)
            if not getattr(self, field.name) or not getattr(self, field.name).strip()
        ]

    def get_step_word_count(self, step_name: str) -> int:
        """
        Get word count for a specific step.

        Args:
            step_name: Name of the step ('step_1', 'step_2', etc.)

        Returns:
            int: Word count for the specified step, 0 if step is None/empty
        """
        content = getattr(self, step_name, None)
        if not content:
            return 0
        return len(content.split())

    def get_final_description_word_count(self) -> int:
        """
        Get word count for the final description.

        Returns:
            int: Word count for final description, 0 if None/empty
        """
        if not self.final_description:
            return 0
        return len(self.final_description.split())


class GeneratorAgent:
    """GeneratorAgent class for generating weather charts scientific descriptions."""

    def __init__(
        self, llm: BaseLLM, system_prompt: str | None, user_prompt: str
    ) -> None:
        """
        Initialize the GeneratorAgent with a BaseLLM instance.

        Args:
            llm (BaseLLM): An instance of a BaseLLM to handle LLM interactions.
        """
        self.llm = llm
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

    def generate(
        self, figure: ekp.Figure | None = None, image: ImageFile | None = None
    ) -> str:
        """
        Generate a structured weather description using the LLM.

        Args:
            figure (Figure | None): Optional figure to include in the request. Can't be used with image.
            image (ImageFile | None): Optional image to include in the request (will be converted to base64). Can't be used with figure.

        Returns:
            str: The final weather description.

        Raises:
            ValueError: If the output string is empty or None.
            RuntimeError: For other run-time errors.
            Exception: If the LLM response is incomplete or parsing fails.
        """
        if figure is not None and image is not None:
            raise ValueError(
                "Only one of 'figure' or 'image' can be provided, not both."
            )
        if figure is not None:
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
            response = self.llm.generate(
                user_prompt=self.user_prompt,
                system_prompt=self.system_prompt,
                image=image,
            )

            parsed_output = self.parse_llm_response(response)
            if not parsed_output.is_complete():
                raise ValueError(
                    "Parsed output is incomplete. Missing fields: "
                    f"{parsed_output.get_missing_fields()}"
                )

            description = parsed_output.final_description

        except Exception as e:
            raise RuntimeError(f"Failed to generate response: {e}") from e

        return description  # type: ignore[return-value]

    def parse_llm_response(self, response: str) -> GeneratorOutput:
        """
        Parse the XML-tagged response from the generator agent into structured data.

        Args:
            response (str): The full llm response string containing XML tags

        Returns:
            GeneratorOutput: Parsed content with individual step results

        Raises:
            ValueError: If the response string is empty or None
            Exception: If parsing fails for any step
        """
        if not response or not response.strip():
            raise ValueError("Response string is empty or None")

        result = GeneratorOutput()

        patterns = {
            field.name: rf"<{field.name}>(.*?)</{field.name}>"
            for field in fields(GeneratorOutput)
        }

        for field_name, pattern in patterns.items():
            try:
                match = re.search(pattern, response, re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    if content:
                        setattr(result, field_name, content)
            except Exception as e:
                print(f"Warning: Failed to parse {field_name}: {e}")
                continue

        return result

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
        self, user_prompt: str, metadata: "FigureMetadata"
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
