#!/usr/bin/env python3
"""
CLI entrypoint for generating weather chart descriptions.
"""

import logging
import os
import sys
from pathlib import Path

import fire
from dotenv import load_dotenv
from PIL import Image

from earth_reach_agent.core.generator import GeneratorAgent
from earth_reach_agent.core.llm import BaseLLM, GroqLLM, OpenAILLM
from earth_reach_agent.core.prompts import DEFAULT_USER_PROMPT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

load_dotenv()


def load_prompt_from_file(file_path: str) -> str:
    """
    Load prompt text from a file.

    Args:
        file_path (str): Path to the text file containing the prompt

    Returns:
        str: The loaded prompt text

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file can't be read
        ValueError: If file is empty
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Prompt file not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                raise ValueError(f"Prompt file is empty: {file_path}")
            return content
    except Exception as e:
        raise IOError(f"Failed to read prompt file '{file_path}': {e}")


def resolve_prompt(
    direct_prompt: str | None,
    file_path: str | None,
    default_prompt: str | None,
) -> str | None:
    """
    Resolve final prompt from direct string, file path, or default.

    Args:
        direct_prompt (str | None): Direct prompt text
        file_path (str | None): Path to prompt file
        default_prompt (str | None): Default prompt to use if neither is provided

    Returns:
        str | None: The resolved prompt text

    Raises:
        ValueError: If both direct_prompt and file_path are provided
    """
    if direct_prompt is not None and file_path is not None:
        raise ValueError(
            "Cannot specify both prompt file and prompt text. Please use only one."
        )

    if direct_prompt is not None:
        if not direct_prompt.strip():
            raise ValueError("Prompt text is an empty string.")
        return direct_prompt.strip()

    if file_path is not None:
        return load_prompt_from_file(file_path)

    return default_prompt


def validate_image_path(image_path: str) -> Path:
    """
    Validate that image path exists and is a supported format.

    Args:
        image_path (str): Path to the image file

    Returns:
        Path: Validated Path object

    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image format is not supported
    """
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {image_path}")

    valid_extensions = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}
    if path.suffix not in valid_extensions:
        raise ValueError(
            f"Unsupported image format: {path.suffix}. "
            f"Supported formats: {', '.join(sorted(valid_extensions))}"
        )

    return path


def create_llm(provider="groq") -> BaseLLM:
    """
    Create and return LLM instance.

    This function can be modified to support different LLM configurations
    or to read from environment variables/config files.

    Args:
        provider (str): LLM provider name (default: "groq")

    Returns:
        BaseLLM: Configured LLM instance
    """
    if provider.lower() == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set.")
        return GroqLLM(
            model_name="meta-llama/llama-4-maverick-17b-128e-instruct", api_key=api_key
        )
    elif provider.lower() == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        return OpenAILLM(model_name="o4-mini-2025-04-16", api_key=api_key)
    else:
        raise ValueError(
            f"Unsupported LLM provider: {provider}. Supported providers: 'groq', 'openai'."
        )


def main(
    image_path: str,
    system_prompt: str | None = None,
    system_prompt_file_path: str | None = None,
    user_prompt: str | None = None,
    user_prompt_file_path: str | None = None,
    verbose: bool = False,
) -> None:
    """
    Generate a scientific description of a weather chart from an image.

    Args:
        image_path (str): Path to the weather chart image (JPEG or PNG)
        system_prompt (str | None): System prompt text (optional)
        system_prompt_file_path (str | None): Path to system prompt file (optional)
        user_prompt (str | None): User prompt text (optional)
        user_prompt_file_path (str | None): Path to user prompt file (optional)
        verbose (bool): Enable verbose output (optional)

    Returns:
        None: Prints the generated weather description

    Raises:
        FileNotFoundError: If image or prompt files don't exist
        ValueError: If arguments are invalid or conflicting
        RuntimeError: If description generation fails
    """
    try:
        if verbose:
            logger.info(f"Validating image: {image_path}")
        validated_image_path = validate_image_path(image_path)
        image = Image.open(validated_image_path)

        if verbose:
            logger.info("Resolving prompts...")
        system_prompt_text = resolve_prompt(
            system_prompt,
            system_prompt_file_path,
            None,
        )
        user_prompt_text = resolve_prompt(
            user_prompt, user_prompt_file_path, DEFAULT_USER_PROMPT
        )
        if not user_prompt_text:
            raise ValueError(
                "User prompt cannot be empty. Please provide a valid prompt."
            )

        if verbose:
            if system_prompt_text:
                logger.info(
                    f"System prompt length: {len(system_prompt_text)} characters"
                )

            if user_prompt_text:
                logger.info(f"User prompt length: {len(user_prompt_text)} characters")

        if verbose:
            logger.info("Initializing LLM...")
        llm = create_llm()

        if verbose:
            logger.info("Creating generator agent...")
        generator = GeneratorAgent(
            llm=llm, system_prompt=system_prompt_text, user_prompt=user_prompt_text
        )

        if verbose:
            logger.info(f"Generating description for: {validated_image_path.name}")
        description = generator.generate(image=image)

        if verbose:
            logger.info("Description generated successfully!")
            logger.info(f"Description length: {len(description)} characters")
            logger.info("-" * 50)

        print(description)

        return None

    except (FileNotFoundError, ValueError, IOError) as e:
        logger.error(f"Could not load image file: {e}", exc_info=True)
        sys.exit(1)
    except RuntimeError as e:
        logger.error(f"Generation failed: {e}", exc_info=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


def cli():
    """
    CLI entrypoint for generating weather chart descriptions.
    """
    fire.Fire(main)


if __name__ == "__main__":
    cli()
