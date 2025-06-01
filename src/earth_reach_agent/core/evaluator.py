class EvaluatorAgent:
    """EvaluatorAgent class for evaluating the quality of Generator Agent's weather chart descriptions."""

    def __init__(self) -> None:
        """
        Initialize the EvaluatorAgent.

        Args:
            parameters, quality criteria, etc..
        """
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
