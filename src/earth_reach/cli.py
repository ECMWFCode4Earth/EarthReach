#!/usr/bin/env python3
"""
CLI entrypoint for generating weather chart descriptions.
"""

import os
import sys

from pathlib import Path

import fire

from dotenv import load_dotenv
from PIL import Image

from earth_reach.config.criteria import QualityCriteria
from earth_reach.config.logging import get_logger
from earth_reach.core.evaluator import EvaluatorAgent
from earth_reach.core.generator import GeneratorAgent
from earth_reach.core.llm import create_llm
from earth_reach.core.orchestrator import Orchestrator
from earth_reach.core.prompts.generator import get_default_generator_user_prompt

logger = get_logger(__name__)

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
        with open(file_path, encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                raise ValueError(f"Prompt file is empty: {file_path}")
            return content
    except Exception as e:
        raise OSError(f"Failed to read prompt file '{file_path}': {e}") from e


def resolve_prompt(
    direct_prompt: str | None,
    file_path: str | None,
    DEFAULT_USER_PROMPT: str | None,
) -> str | None:
    """
    Resolve final prompt from direct string, file path, or default.

    Args:
        direct_prompt (str | None): Direct prompt text
        file_path (str | None): Path to prompt file
        DEFAULT_USER_PROMPT (str | None): Default prompt to use if neither is provided

    Returns:
        str | None: The resolved prompt text

    Raises:
        ValueError: If both direct_prompt and file_path are provided
    """
    if direct_prompt is not None and file_path is not None:
        raise ValueError(
            "Cannot specify both prompt file and prompt text. Please use only one.",
        )

    if direct_prompt is not None:
        if not direct_prompt.strip():
            raise ValueError("Prompt text is an empty string.")
        return direct_prompt.strip()

    if file_path is not None:
        return load_prompt_from_file(file_path)

    return DEFAULT_USER_PROMPT


def resolve_description(
    description: str | None,
    description_file_path: str | None,
) -> str | None:
    """
    Resolve description from multiple sources with priority: direct text > file.

    Args:
        description (str | None): Direct description text
        description_file_path (str | None): Path to description file

    Returns:
        str | None: Resolved description text

    Raises:
        ValueError: If both description sources are provided or file is invalid
        FileNotFoundError: If description file doesn't exist
    """
    if description and description_file_path:
        raise ValueError(
            "Cannot provide both description text and description file path. "
            "Please provide only one.",
        )

    if description:
        return description

    if description_file_path:
        if not os.path.exists(description_file_path):
            raise FileNotFoundError(
                f"Description file not found: {description_file_path}",
            )

        try:
            with open(description_file_path, encoding="utf-8") as file:
                return file.read().strip()
        except Exception as e:
            raise ValueError(f"Error reading description file: {e}") from e

    return None


def get_valid_criteria() -> list[str]:
    """
    Get list of valid evaluation criteria.

    Returns:
        List[str]: List of valid criteria names
    """
    return QualityCriteria.list()


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
            f"Supported formats: {', '.join(sorted(valid_extensions))}",
        )

    return path


class CLI:
    """
    Command Line Interface for the Earth Reach Agent.
    Allows users to generate and evaluate weather chart descriptions from images.
    """

    @staticmethod
    def generate(
        image_path: str,
        system_prompt: str | None = None,
        system_prompt_file_path: str | None = None,
        user_prompt: str | None = None,
        user_prompt_file_path: str | None = None,
        simple: bool = False,
        max_iterations: int = 3,
        criteria_threshold: int = 4,
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
            simple (bool): Skip orchestrator to only use generator (optional)
            max_iterations (int): Orchestrator maximum iterations for description generation (default: 3)
            criteria_threshold (int): Minimum score for evaluation criteria to pass (default: 4
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
                user_prompt,
                user_prompt_file_path,
                get_default_generator_user_prompt(),
            )
            if not user_prompt_text:
                raise ValueError(
                    "User prompt cannot be empty. Please provide a valid prompt.",
                )

            if verbose:
                if system_prompt_text:
                    logger.info(
                        f"System prompt length: {len(system_prompt_text)} characters",
                    )

                if user_prompt_text:
                    logger.info(
                        f"User prompt length: {len(user_prompt_text)} characters",
                    )

            if verbose:
                logger.info("Initializing LLM...")
            llm = create_llm()

            if verbose:
                logger.info("Creating generator agent...")

            generator = GeneratorAgent(
                llm=llm,
                system_prompt=system_prompt_text,
                user_prompt=user_prompt_text,
            )

            if not simple:
                if verbose:
                    logger.info("Creating evaluator agent...")

                evaluator = EvaluatorAgent(
                    criteria=QualityCriteria.list(),
                    llm=llm,
                )

                if verbose:
                    logger.info("Creating orchestrator...")

                orchestrator = Orchestrator(
                    generator_agent=generator,
                    evaluator_agent=evaluator,
                    max_iterations=max_iterations,
                    criteria_threshold=criteria_threshold,
                )

            if verbose:
                logger.info(f"Generating description for: {validated_image_path.name}")

            if simple:
                description = generator.generate(
                    image=image,
                    return_intermediate_steps=False,
                )
            else:
                description = orchestrator.run(image=image)

            if verbose and isinstance(description, str):
                logger.info("Description generated successfully!")
                logger.info(f"Description length: {len(description)} characters")
                logger.info("-" * 50)

            print(description)

            return

        except (OSError, FileNotFoundError, ValueError) as e:
            logger.error(f"Could not load image file: {e}", exc_info=True)
            sys.exit(1)
        except RuntimeError as e:
            logger.error(f"Generation failed: {e}", exc_info=True)
            sys.exit(1)
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            sys.exit(1)

    @staticmethod
    def evaluate(
        image_path: str,
        description: str | None = None,
        description_file_path: str | None = None,
        criteria: list[str] | None = None,
        verbose: bool = False,
    ) -> None:
        """
        Evaluate a generated weather chart description.

        Args:
            image_path (str): Path to the weather chart image (JPEG or PNG)
            description (str | None): The description text to evaluate (optional)
            description_file_path (str | None): Path to file containing description (optional)
            criteria (List[str]): List of evaluation criteria to assess
            verbose (bool): Enable verbose output (optional)

        Returns:
            None: Prints evaluation results

        Raises:
            FileNotFoundError: If image or description files don't exist
            ValueError: If arguments are invalid or conflicting
            RuntimeError: If evaluation fails
        """
        if criteria is None:
            criteria = ["coherence", "fluency", "consistency", "relevance"]

        try:
            if verbose:
                logger.info(f"Validating image: {image_path}")

            validated_image_path = validate_image_path(image_path)
            image = Image.open(validated_image_path)

            if verbose:
                logger.info("Resolving description...")

            description_text = resolve_description(
                description,
                description_file_path,
            )
            if not description_text or description_text.strip() == "":
                raise ValueError(
                    "Description cannot be empty. Please provide a valid description.",
                )

            if verbose:
                logger.info(f"Description length: {len(description_text)} characters")

            if not criteria or len(criteria) == 0:
                raise ValueError("Criteria list cannot be empty.")

            valid_criteria = get_valid_criteria()
            invalid_criteria = [c for c in criteria if c not in valid_criteria]
            if invalid_criteria:
                raise ValueError(
                    f"Invalid criteria: {invalid_criteria}. Valid criteria are: {valid_criteria}",
                )

            if verbose:
                logger.info(f"Evaluation criteria: {', '.join(criteria)}")

            if verbose:
                logger.info("Initializing LLM...")
            llm = create_llm()

            if verbose:
                logger.info("Creating evaluator agent...")
            evaluator = EvaluatorAgent(
                criteria=criteria,
                llm=llm,
            )

            if verbose:
                logger.info(f"Evaluating description for: {validated_image_path.name}")
            evaluation = evaluator.evaluate(
                description=description_text,
                image=image,
            )

            if verbose:
                logger.info("Evaluation completed successfully!")
                logger.info(f"Number of criteria evaluated: {len(evaluation)}")
                logger.info("-" * 50)

            for eval in evaluation:
                print(f"Criterion: {eval.name}")
                print(f"Score: {eval.score}/5")
                if verbose:
                    print(f"Reasoning: {eval.reasoning}")
                print("-" * 50)

            return

        except FileNotFoundError as e:
            logger.error(f"File not found: {e}", exc_info=True)
            sys.exit(1)
        except ValueError as e:
            logger.error(f"Invalid input: {e}", exc_info=True)
            sys.exit(1)
        except Exception as e:
            logger.error(f"Evaluation failed: {e}", exc_info=True)
            sys.exit(1)


def cli() -> None:
    """
    CLI entrypoint.
    """
    fire.Fire(CLI)


if __name__ == "__main__":
    cli()
