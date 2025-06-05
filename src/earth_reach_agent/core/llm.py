import openai

from earth_reach_agent.core.utils import img_to_base64


class BaseLLM:
    """Base class for a LLM interface."""

    def __init__(
        self,
        model_name: str,
        base_url: str,
        api_key: str | None = None,
    ) -> None:
        """
        Initialize the LLM with a model name and optional keyword arguments.

        Args:
            model_name (str): The name of the model to use.
            base_url (str): The base URL for the LLM API.
            api_key (str | None): The API key for authentication with the LLM provider.
            **kwargs: Additional keyword arguments for the LLM configuration.
        """
        self.model_name = model_name
        self.base_url = base_url
        self.api_key = api_key

        self.client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    def generate(
        self, user_prompt: str, system_prompt: str | None = None, image=None
    ) -> str:
        """
        Generate a response from the LLM API based on the user prompt and optional system prompt.

        Args:
            user_prompt (str): The prompt provided by the user to define the task.
            system_prompt (str | None): An optional system prompt to guide the model's response.
            image: Optional image to include in the request (will be converted to base64).

        Returns:
            str: The generated response content from the LLM.

        Raises:
            ValueError: If user_prompt is empty/None or if the API response is empty.
            RuntimeError: For other run-time errors.
        """

        if not user_prompt or not user_prompt.strip():
            raise ValueError("user_prompt cannot be empty or None")

        messages = []

        if system_prompt and system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt.strip()})

        try:
            if image:
                base64_image = img_to_base64(img=image)
                if not base64_image:
                    raise ValueError("Failed to convert image to base64")

                user_content = [
                    {"type": "text", "text": user_prompt.strip()},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ]
            else:
                user_content = user_prompt.strip()

            messages.append({"role": "user", "content": user_content})

        except Exception as e:
            raise ValueError(f"Failed to process input data: {e}")

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
            )

            content = response.choices[0].message.content

            if not content or not content.strip():
                raise ValueError("The generated response content is empty")

            return content.strip()

        except ValueError:
            raise
        except Exception as e:
            error_msg = f"API call failed: {type(e).__name__}: {e}"
            print(error_msg)
            raise RuntimeError(error_msg) from e

    def __repr__(self) -> str:
        return f"LLM(model_name={self.model_name}, base_url={self.base_url})"


class GroqLLM(BaseLLM):
    """Implementation of the BaseLLM for Groq LLM API Provider."""

    def __init__(self, model_name: str, api_key: str | None = None) -> None:
        """Initialize the Groq LLM with a model name and optional API key.

        Args:
            model_name (str): The name of the Groq model to use.
            api_key (str | None): The API key for authentication with the Groq API.

        Raises:
            AssertionError: If the API key is not provided and not found in environment variables.
        """

        if not api_key:
            import os

            api_key = os.environ.get("GROQ_API_KEY", None)
            if not api_key:
                raise AssertionError(
                    "GROQ_API_KEY not set. Please set it in your environment variables, or pass it as an argument."
                )

        super().__init__(
            model_name=model_name, api_key=api_key, base_url="https://api.groq.com/v1"
        )


class OpenAILLM(BaseLLM):
    """Implementation of the BaseLLM for OpenAI API Provider."""

    def __init__(self, model_name: str, api_key: str | None = None) -> None:
        """Initialize the OpenAI LLM with a model name and optional API key.

        Args:
            model_name (str): The name of the OpenAI model to use.
            api_key (str | None): The API key for authentication with the OpenAI API.

        Raises:
            AssertionError: If the API key is not provided and not found in environment variables.
        """

        if not api_key:
            import os

            api_key = os.environ.get("OPENAI_API_KEY", None)
            if not api_key:
                raise AssertionError(
                    "OPENAI_API_KEY not set. Please set it in your environment variables, or pass it as an argument."
                )

        super().__init__(
            model_name=model_name, api_key=api_key, base_url="https://api.openai.com/v1"
        )
