import re
from dataclasses import dataclass
from typing import List, Optional

from earth_reach_agent.core.llm import BaseLLM


class GeneratorAgent:
    """GeneratorAgent class for generating weather charts scientific descriptions."""

    def __init__(self, llm: BaseLLM) -> None:
        """
        Initialize the GeneratorAgent with a BaseLLM instance.

        Args:
            llm (BaseLLM): An instance of a BaseLLM to handle LLM interactions.
        """
        self.llm = llm


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

    step_1: Optional[str] = None
    step_2: Optional[str] = None
    step_3: Optional[str] = None
    step_4: Optional[str] = None
    final_description: Optional[str] = None

    def is_complete(self) -> bool:
        """
        Check if all required fields were successfully parsed.

        Returns:
            bool: True if all fields contain content, False otherwise
        """
        return all(
            [
                self.step_1 is not None and self.step_1.strip(),
                self.step_2 is not None and self.step_2.strip(),
                self.step_3 is not None and self.step_3.strip(),
                self.step_4 is not None and self.step_4.strip(),
                self.final_description is not None and self.final_description.strip(),
            ]
        )

    def get_missing_fields(self) -> List[str]:
        """
        Return list of field names that were not successfully parsed.

        Returns:
            List[str]: Names of fields that are None or empty
        """
        missing = []
        if not self.step_1 or not self.step_1.strip():
            missing.append("step_1")
        if not self.step_2 or not self.step_2.strip():
            missing.append("step_2")
        if not self.step_3 or not self.step_3.strip():
            missing.append("step_3")
        if not self.step_4 or not self.step_4.strip():
            missing.append("step_4")
        if not self.final_description or not self.final_description.strip():
            missing.append("final_description")
        return missing

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


# TODO(high): refactor this to add it to the generator agent class
def parse_generator_output(output: str) -> GeneratorOutput:
    """
    Parse the XML-tagged output from the generator agent into structured data.

    Args:
        output (str): The full output string containing XML tags

    Returns:
        GeneratorOutput: Parsed content with individual step results

    Raises:
        ValueError: If the output string is empty or None
    """
    if not output or not output.strip():
        raise ValueError("Output string is empty or None")

    result = GeneratorOutput()

    patterns = {
        "step_1": r"<step_1>(.*?)</step_1>",
        "step_2": r"<step_2>(.*?)</step_2>",
        "step_3": r"<step_3>(.*?)</step_3>",
        "step_4": r"<step_4>(.*?)</step_4>",
        "final_description": r"<final_description>(.*?)</final_description>",
    }

    for field_name, pattern in patterns.items():
        try:
            match = re.search(pattern, output, re.DOTALL)
            if match:
                content = match.group(1).strip()
                if content:
                    setattr(result, field_name, content)
        except Exception as e:
            print(f"Warning: Failed to parse {field_name}: {e}")
            continue

    return result


def validate_generator_output(
    parsed_output: GeneratorOutput, require_all_steps: bool = True
) -> tuple[bool, List[str]]:
    """
    Validate that the parsed output meets expected criteria.

    Args:
        parsed_output: The parsed GeneratorOutput object
        require_all_steps: Whether to require all steps to be present

    Returns:
        tuple[bool, List[str]]: (is_valid, list_of_issues)
    """
    issues = []

    if require_all_steps:
        missing = parsed_output.get_missing_fields()
        if missing:
            issues.append(f"Missing required fields: {', '.join(missing)}")

    final_word_count = parsed_output.get_final_description_word_count()
    if parsed_output.final_description and (
        final_word_count < 300 or final_word_count > 500
    ):
        issues.append(
            f"Final description word count ({final_word_count}) outside expected range (300-500)"
        )

    if not parsed_output.final_description:
        issues.append("Final description is missing or empty")

    is_valid = len(issues) == 0
    return is_valid, issues
