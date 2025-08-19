"""
Orchestrator module.

This module provides the orchestrator class, driving the generator and evaluator successive
interactions to generate high-quality weather chart descriptions.
"""

import earthkit.data as ekd
import earthkit.plots as ekp

from PIL.ImageFile import ImageFile

from earth_reach.config.logging import get_logger
from earth_reach.core.evaluator import CriterionEvaluatorOutput, EvaluatorAgent
from earth_reach.core.extractors.base_extractor import (
    BaseDataExtractor,
)
from earth_reach.core.generator import GeneratorAgent, GeneratorOutput
from earth_reach.core.prompts.orchestrator import get_default_feedback_template

logger = get_logger(__name__)


class Orchestrator:
    """Orchestrates Generator and Evaluator agents to create weather chart descriptions."""

    def __init__(
        self,
        generator_agent: GeneratorAgent,
        evaluator_agent: EvaluatorAgent,
        data_extractors: list[BaseDataExtractor] | None = None,
        max_iterations: int = 3,
        criteria_threshold: int = 4,
        feedback_template: str | None = None,
    ) -> None:
        """
        Initialize the orchestrator with generator and evaluator agents.

        Args:
            generator_agent: Instance of GeneratorAgent for generating descriptions
            evaluator_agent: Instance of EvaluatorAgent for evaluating descriptions
            data_extractors: List of BaseDataExtractor instances for extracting features
            max_iterations: Maximum number of iterations for generating descriptions
            criteria_threshold: Minimum score for evaluation criteria to pass
            feedback_template: Template for feedback to the generator agent (optional)
        """
        self.generator_agent = generator_agent
        self.evaluator_agent = evaluator_agent
        self.data_extractors = data_extractors if data_extractors is not None else []

        self.max_iterations = max_iterations
        if self.max_iterations <= 0:
            raise ValueError("max_iterations must be greater than 0")

        self.criteria_threshold = criteria_threshold
        if self.criteria_threshold < 0 or self.criteria_threshold > 5:
            raise ValueError("criteria_threshold must be between 0 and 5")

        self.feedback_template = feedback_template or get_default_feedback_template()
        self.criteria_limits_acknowledgment = {
            "coherence": "Warning: The logical flow and organization of this description may be unclear.",
            "fluency": "Warning: This description may contain linguistic issues, technical terminology errors, or unclear phrasing.",
            "consistency": "Warning: This description may contain inaccuracies relative to the source chart or internal contradictions.",
            "relevance": "Warning: This description may not adequately emphasize the most meteorologically significant patterns.",
        }

    def run(
        self,
        figure: ekp.Figure | None = None,
        image: ImageFile | None = None,
        data: ekd.FieldList | None = None,
    ) -> str:
        """
        Run the iterative process of generating and evaluating a weather chart description until quality criteria are met.

        Args:
            figure (Figure | None): Optional figure to use to generate a description. Can't be used with image.
            image (ImageFile | None): Optional image to use to generate a description (will be converted to base64). Can't be used with figure.
            data (FieldList | None): Optional data to use to generate a description.

        Returns:
            str: The final weather description.

        Raises:
            RuntimeError: if an error occurs during description generation
        """
        if figure is not None and image is not None:
            raise ValueError(
                "Only one of 'figure' or 'image' can be provided, not both.",
            )

        for extractor in self.data_extractors:
            try:
                features = extractor.extract(data)
                features_str = extractor.format_features_to_str(features)
                self._add_data_features_to_agent_prompt(features_str, agent="generator")
                self._add_data_features_to_agent_prompt(features, agent="evaluator")
            except Exception:
                continue

        try:
            description: str | GeneratorOutput = ""
            evaluation: list[CriterionEvaluatorOutput] = []
            for i in range(self.max_iterations):
                description = self.generator_agent.generate(
                    figure=figure,
                    image=image,
                    return_intermediate_steps=False,
                )
                if not isinstance(description, str):
                    raise TypeError(
                        f"Expected description to be a string, got {type(description)}",
                    )

                if not description:
                    raise ValueError("Generated description is empty.")

                evaluation = self.evaluator_agent.evaluate(
                    description,
                    image=image,
                    figure=figure,
                )

                if self._verify_evaluation_passes(evaluation):
                    return description

                self._provide_feedback_to_generator(i + 1, description, evaluation)

            logger.info(
                "Maximum iterations %d reached without passing evaluation. Acknowledging limits of description.",
                self.max_iterations,
            )

            if not isinstance(description, str):
                raise TypeError(
                    f"Expected description to be a string, got {type(description)}",
                )
            if not description:
                raise ValueError("Final generated description is empty.")

            return self._acknowledge_limits_of_description(
                description,
                evaluation,
            )
        except Exception as e:
            raise RuntimeError("Failed to generate a description") from e

    def _add_data_features_to_agent_prompt(self, features: str, agent: str) -> None:
        """Add extracted data features to end of agent prompt

        Args:
            features (str): extracted and string formatted data features
            agent (str): agent to add the prompt to
        """
        if agent not in ["generator", "evaluator"]:
            raise ValueError(
                f"agent parameter should be one of ['generator', 'evaluator'], found {agent}"
            )

        if agent == "generator":
            self.generator_agent.append_user_prompt(features)

        self.evaluator_agent.append_user_prompt(features)

    def _verify_evaluation_passes(
        self,
        evaluation: list[CriterionEvaluatorOutput],
    ) -> bool:
        """
        Verify if the evaluation passes the quality criteria.

        Args:
            evaluation (List[CriterionEvaluatorOutput]): Evaluation results from the EvaluatorAgent

        Returns:
            bool: True if evaluation passes, False otherwise
        """
        return all(
            criterion.score >= self.criteria_threshold for criterion in evaluation
        )

    def _provide_feedback_to_generator(
        self,
        evaluation_id: int,
        description: str,
        evaluation: list[CriterionEvaluatorOutput],
    ) -> None:
        """
        Provide feedback to the GeneratorAgent based on evaluation results.

        Args:
            description (str): The description generated by the GeneratorAgent
            evaluation (List[CriterionEvaluatorOutput]): Evaluation results from the EvaluatorAgent
        """
        unmet_criteria = [
            criterion
            for criterion in evaluation
            if criterion.score < self.criteria_threshold
        ]
        if not unmet_criteria:
            logger.warning("No unmet criteria found in evaluation.")
            return

        feedback = self.feedback_template.format(
            evaluation_id=evaluation_id,
            criteria_scores="\n- ".join(
                f"- {criterion.name}: {criterion.score}/5"
                for criterion in unmet_criteria
            ),
            criteria_reasoning="\n".join(
                f"- {criterion.name}: {criterion.reasoning or 'No reasoning available'}"
                for criterion in unmet_criteria
            ),
            description=description,
        )

        self.generator_agent.append_user_prompt(feedback)

    def _acknowledge_limits_of_description(
        self,
        description: str,
        evaluation: list[CriterionEvaluatorOutput],
    ) -> str:
        """
        Acknowledge the limits of the generated description based on evaluation results.

        Args:
            description (str): The description generated by the GeneratorAgent
            evaluation (List[CriterionEvaluatorOutput]): Evaluation results from the EvaluatorAgent
        Returns:
            str: The description with acknowledgment of its limits added
        """
        acknowledgment = "\n"
        for criterion in evaluation:
            if criterion.score < self.criteria_threshold:
                crit_ackn = self.criteria_limits_acknowledgment.get(criterion.name, "")
                if crit_ackn:
                    acknowledgment += f"\n{crit_ackn}"
        return description
