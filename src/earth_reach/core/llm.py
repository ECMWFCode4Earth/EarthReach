"""
LLM Interface module.

Provides an abstract interface and concrete implementations for various
Large Language Model providers including OpenAI, Google Gemini, and Anthropic Claude.
"""

import os

from abc import ABC, abstractmethod
from typing import Any

import openai

from google import genai
from google.genai import types
from PIL.ImageFile import ImageFile

from earth_reach.config.logging import get_logger
from earth_reach.core.utils import img_to_base64, img_to_bytes

logger = get_logger(__name__)


class LLMInterface(ABC):
    """Abstract base class defining the interface for all LLM provider implementations."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Must be implemented by subclasses to return the provider name."""

    @abstractmethod
    def generate(
        self,
        user_prompt: str,
        system_prompt: str | None = None,
        image: ImageFile | None = None,
    ) -> str:
        """
        Generate a response from the LLM based on the user prompt and optional system prompt.

        Args:
            user_prompt (str): The prompt provided by the user to define the task.
            system_prompt (str | None): An optional system prompt to guide the model's response.
            image: Optional image to include in the request.

        Returns:
            str: The generated response content from the LLM.

        Raises:
            ValueError: If user_prompt is empty/None or if the API response is empty.
            RuntimeError: For other run-time errors.
        """


class OpenAICompatibleLLM(LLMInterface):
    """Base class for OpenAI-compatible LLM implementations (Groq, OpenAI, etc.)."""

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

    @property
    def provider_name(self):
        return "openAICompatible"

    def generate(
        self,
        user_prompt: str,
        system_prompt: str | None = None,
        image: ImageFile | None = None,
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

        messages: list[Any] = []

        if system_prompt and system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt.strip()})

        try:
            if image:
                base64_image = img_to_base64(img=image)
                if not base64_image:
                    raise ValueError("Failed to convert image to base64")

                user_content: Any = [
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
            raise ValueError(f"Failed to process input data: {e}") from e

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
            )

            content = response.choices[0].message.content

            if not content or not isinstance(content, str) or not content.strip():
                raise ValueError(
                    "The generated response content is empty or not a string"
                )

            logger.info(
                "LLM API call completed successfully",
                extra={
                    "provider": self.provider_name,
                    "model": self.model_name,
                    "input_length": len(user_prompt),
                    "output_length": len(content),
                    "has_image": image is not None,
                },
            )

            return content.strip()

        except ValueError:
            raise
        except Exception as e:
            logger.error(
                "LLM API call failed",
                extra={
                    "provider": self.provider_name,
                    "model": self.model_name,
                },
                exc_info=True,
            )
            raise RuntimeError("LLM API call failed") from e

    def __repr__(self) -> str:
        return f"LLM(model_name={self.model_name}, base_url={self.base_url})"


class GroqLLM(OpenAICompatibleLLM):
    """Implementation of the LLMInterface for Groq LLM API Provider."""

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
                    "GROQ_API_KEY not set. Please set it in your environment variables, or pass it as an argument.",
                )

        super().__init__(
            model_name=model_name,
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )

    @property
    def provider_name(self):
        return "groq"


class OpenAILLM(OpenAICompatibleLLM):
    """Implementation of the LLMInterface for OpenAI API Provider."""

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
                    "OPENAI_API_KEY not set. Please set it in your environment variables, or pass it as an argument.",
                )

        super().__init__(
            model_name=model_name,
            api_key=api_key,
            base_url="https://api.openai.com/v1",
        )

    @property
    def provider_name(self):
        return "openAI"


class GeminiLLM(LLMInterface):
    """Implementation of the LLMInterface for Google Gemini API Provider."""

    def __init__(self, model_name: str, api_key: str | None = None) -> None:
        """Initialize the Gemini LLM with a model name and optional API key.

        Args:
            model_name (str): The name of the Gemini model to use.
            api_key (str | None): The API key for authentication with the Gemini API.

        Raises:
            AssertionError: If the API key is not provided and not found in environment variables.
        """

        if not api_key:
            api_key = os.environ.get("GEMINI_API_KEY", None)
            if not api_key:
                raise AssertionError(
                    "GEMINI_API_KEY not set. Please set it in your environment variables, or pass it as an argument.",
                )

        self.model_name = model_name
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)

    @property
    def provider_name(self):
        return "gemini"

    def generate(
        self,
        user_prompt: str,
        system_prompt: str | None = None,
        image: ImageFile | None = None,
    ) -> str:
        """
        Generate a response from the Gemini API based on the user prompt and optional system prompt.

        Args:
            user_prompt (str): The prompt provided by the user to define the task.
            system_prompt (str | None): An optional system prompt to guide the model's response.
            image: Optional image to include in the request (ImageFile).

        Returns:
            str: The generated response content from the Gemini API.

        Raises:
            ValueError: If user_prompt is empty/None or if the API response is empty.
            RuntimeError: For other run-time errors.
        """

        if not user_prompt or not user_prompt.strip():
            raise ValueError("user_prompt cannot be empty or None")

        try:
            full_prompt = user_prompt.strip()
            if system_prompt and system_prompt.strip():
                full_prompt = f"{system_prompt.strip()}\n\n{user_prompt.strip()}"

            contents: list[Any] = []
            if image:
                image_bytes = img_to_bytes(image)
                if not image_bytes:
                    raise ValueError("Failed to convert image to bytes")

                contents.append(
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/png",
                    ),
                )
            contents.append(full_prompt)

        except Exception as e:
            raise ValueError(f"Failed to process input data: {e}") from e

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
            )

            content = response.text

            if not content or not isinstance(content, str) or not content.strip():
                raise ValueError(
                    "The generated response content is empty or not a string"
                )

            logger.info(
                "LLM API call completed successfully",
                extra={
                    "provider": self.provider_name,
                    "model": self.model_name,
                    "input_length": len(user_prompt),
                    "output_length": len(content),
                    "has_image": image is not None,
                },
            )

            return content.strip()

        except ValueError:
            raise
        except Exception as e:
            logger.error(
                "LLM API call failed",
                extra={
                    "provider": self.provider_name,
                    "model": self.model_name,
                },
                exc_info=True,
            )
            raise RuntimeError("LLM API call failed") from e

    def __repr__(self) -> str:
        return f"GeminiLLM(model_name={self.model_name})"


def create_llm(provider: str = "groq", model_name: str | None = None) -> LLMInterface:
    """
    Create and return LLM instance.

    This function can be modified to support different LLM configurations
    or to read from environment variables/config files.

    Args:
        provider (str): LLM provider name (default: "groq")
        model_name (str | None): Specific model name to use (default: None, uses provider's default)

    Returns:
        LLMInterface: Configured LLM instance
    """
    if provider.lower() == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set.")

        if model_name is None:
            model_name = "meta-llama/llama-4-maverick-17b-128e-instruct"
        return GroqLLM(model_name=model_name, api_key=api_key)

    if provider.lower() == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        if model_name is None:
            model_name = "o4-mini-2025-04-16"
        return OpenAILLM(model_name=model_name, api_key=api_key)

    if provider.lower() == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")

        if model_name is None:
            model_name = "gemini-2.5-flash"
        return GeminiLLM(model_name=model_name, api_key=api_key)

    raise ValueError(
        f"Unsupported LLM provider: {provider}. Supported providers: 'groq', 'openai', 'gemini'.",
    )
