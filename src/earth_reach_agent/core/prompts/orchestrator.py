DEFAULT_FEEDBACK_TEMPLATE = """## EVALUATOR FEEDBACK

Evaluation number: {evaluation_id}

Your last attempt to generate a weather chart description was reviewed by an expert evaluator.

During their review, they deemed that the description did not meet the following quality criteria:
{criteria_scores}

They provided the following reasoning for their evaluation:
{criteria_reasoning}

Here's the description that was evaluated:
{description}

Your will now attempt to improve the description based on this feedback. To achieve this, you will
go through all the reasoning steps defined above, while taking into account the feedback provided by the evaluator.
"""


def get_default_feedback_template() -> str:
    """
    Get the default feedback template for the OrchestratorAgent.

    Returns:
        str: The default feedback template.
    """
    return DEFAULT_FEEDBACK_TEMPLATE
