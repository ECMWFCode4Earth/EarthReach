from earth_reach_agent.core.llm import BaseLLM


class GeneratorAgent:
    def __init__(self, llm: BaseLLM) -> None:
        """
        Initialize the GeneratorAgent with a BaseLLM instance.

        Args:
            llm (BaseLLM): An instance of a BaseLLM to handle LLM interactions.
        """
        self.llm = llm
