"""
Quality criteria module.

Defines the evaluation criteria used to assess the quality of generated
weather chart descriptions across multiple dimensions including coherence and accuracy.
"""

from enum import Enum


class QualityCriteria(Enum):
    COHERENCE = "coherence"
    FLUENCY = "fluency"
    CONSISTENCY = "consistency"
    RELEVANCE = "relevance"

    @classmethod
    def list(cls) -> list[str]:
        return [criterion.value for criterion in cls]
