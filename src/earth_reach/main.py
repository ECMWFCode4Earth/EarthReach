"""
Main module.

Contains the main EarthReachAgent class that serves as the primary
entry point for the dual-LLM weather chart description framework.
"""

from typing import Any

import earthkit.data as ekd
import earthkit.plots as ekp

from earth_reach.config.criteria import QualityCriteria
from earth_reach.config.logging import get_logger
from earth_reach.core.evaluator import EvaluatorAgent
from earth_reach.core.extractors.base_extractor import BaseDataExtractor
from earth_reach.core.extractors.pressure_extractor import PressureCenterDataExtractor
from earth_reach.core.extractors.temperature_extractor import TemperatureDataExtractor
from earth_reach.core.generator import GeneratorAgent
from earth_reach.core.llm import create_llm
from earth_reach.core.orchestrator import Orchestrator
from earth_reach.core.prompts.generator import get_default_generator_user_prompt

logger = get_logger(__name__)


# TODO(high): update so that generation continues if data is none, but just don't instantiate the data extractors and probably log it
# TODO(high): add parameter to use or not data extractors
class EarthReachAgent:
    """
    Main agent class for generating weather chart descriptions.

    This class is meant to be the main entrypoint for the earthkit.plots integration.
    To generate descriptions from images, instead of figure and data objects, use the provided CLI.

    Provides a high-level interface for the dual-LLM framework, handling
    data validation, component initialization, and orchestrated generation.
    """

    def __init__(
        self,
        provider: str,
        model_name: str | None = None,
        max_iterations: int = 3,
        criteria_threshold: int = 4,
    ) -> None:
        """
        Initialize the EarthReachAgent with LLM provider and configuration parameters.

        Args:
            provider: LLM provider name (e.g., "openai", "gemini", "groq", "anthropic")
            model_name: Specific model name to use (optional, uses provider default)
            max_iterations: Maximum number of iterations for the orchestrator
            criteria_threshold: Minimum score for evaluation criteria to pass
        """
        self.provider = provider
        self.model_name = model_name
        self.required_vars = {"2t", "msl"}
        self.max_iterations = max_iterations
        self.criteria_threshold = criteria_threshold
        logger.info(
            "EarthReachAgent initialized with provider=%s, model=%s, max_iterations=%d, criteria_threshold=%d",
            provider,
            model_name or "default",
            max_iterations,
            criteria_threshold,
        )

    def _validate_inputs(self, figure: Any, data: Any) -> None:
        """
        Validate that inputs are of the correct types and contain required data.

        Args:
            figure: Should be an earthkit.plots.Figure object
            data: Should be an earthkit.data.FieldList object

        Raises:
            TypeError: If inputs are not of the expected types
            ValueError: If required variables are missing from data
        """
        logger.debug("Validating inputs...")

        if not isinstance(figure, ekp.Figure):
            raise TypeError(f"Expected earthkit.plots.Figure, got {type(figure)}")

        if not isinstance(data, ekd.FieldList):
            raise TypeError(f"Expected earthkit.data.FieldList, got {type(data)}")

        available_vars = set()
        try:
            for field in data:
                param = field.metadata("param")
                if param:
                    available_vars.add(param)
        except Exception as e:
            logger.warning("Could not extract parameter metadata from data: %s", e)
            return

        missing_vars = self.required_vars - available_vars
        if missing_vars:
            raise ValueError(f"Required variables missing from data: {missing_vars}")

    def _create_data_extractors(self, data: ekd.FieldList) -> list[BaseDataExtractor]:
        """
        Create appropriate data extractors based on available variables in the data.

        Args:
            data: FieldList containing GRIB data

        Returns:
            List of data extractor instances

        Raises:
            RuntimeError: If extractor creation fails
        """
        logger.debug("Creating data extractors...")
        extractors = []

        available_vars = set()
        for field in data:
            param = field.metadata("param")
            if param:
                available_vars.add(param)

        if "2t" in available_vars:
            try:
                extractors.append(TemperatureDataExtractor())
                logger.debug("Temperature data extractor created")
            except Exception as e:
                logger.debug("Could not create temperature data extractor: %s", e)

        if "msl" in available_vars:
            try:
                extractors.append(PressureCenterDataExtractor())
                logger.debug("Pressure centers data extractor created")
            except Exception as e:
                logger.debug("Could not create pressure centers data extractor: %s", e)

        logger.info("Created %d data extractors", len(extractors))
        return extractors

    def _setup_components(
        self, data_extractors: list[BaseDataExtractor]
    ) -> Orchestrator:
        """
        Initialize LLM, agents, and orchestrator with the provided data extractors.

        Args:
            data_extractors: List of data extractor instances

        Returns:
            Configured orchestrator instance

        Raises:
            RuntimeError: If component setup fails
        """
        try:
            logger.debug("Initializing components...")
            llm = create_llm(provider=self.provider, model_name=self.model_name)

            generator = GeneratorAgent(
                llm=llm,
                system_prompt=None,
                user_prompt=get_default_generator_user_prompt(),
            )

            evaluator = EvaluatorAgent(
                criteria=QualityCriteria.list(),
                llm=llm,
            )

            orchestrator = Orchestrator(
                generator_agent=generator,
                evaluator_agent=evaluator,
                data_extractors=data_extractors,
                max_iterations=self.max_iterations,
                criteria_threshold=self.criteria_threshold,
            )

            logger.info("Component setup completed successfully")
            return orchestrator

        except Exception as e:
            raise RuntimeError(f"Failed to setup components: {e}") from e

    def generate_alt_description(
        self, figure: ekp.Figure, data: ekd.FieldList, use_extractors: bool = False
    ) -> str:
        """
        Generate alternative text description for a weather chart.

        Args:
            figure: earthkit.plots Figure object containing the weather chart
            data: earthkit.data FieldList containing GRIB meteorological data
            use_extractors: Whether to use data extractors to enrich prompt or not. Default to False

        Returns:
            String description of the weather chart

        Raises:
            TypeError: If inputs are not of the expected types
            ValueError: If required data is missing or invalid
            RuntimeError: If description generation fails
        """
        try:
            logger.info("Starting description generation...")

            self._validate_inputs(figure, data)

            if use_extractors:
                logger.info("Creating data extractors to enrich prompts")
                data_extractors = self._create_data_extractors(data)
            else:
                data_extractors = []

            orchestrator = self._setup_components(data_extractors)

            logger.info("Running orchestrated description generation...")
            description = orchestrator.run(figure=figure, data=data)

            if not isinstance(description, str):
                raise TypeError(f"Expected string description, got {type(description)}")

            if not description.strip():
                raise ValueError("Generated description is empty")

            logger.info(
                "Description generation completed successfully (length: %d characters)",
                len(description),
            )
            return description.strip()

        except (TypeError, ValueError) as e:
            logger.error("Input validation or data error: %s", e)
            raise
        except RuntimeError as e:
            logger.error("Runtime error during generation: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error during description generation: %s", e)
            raise RuntimeError(f"Failed to generate description: {e}") from e
