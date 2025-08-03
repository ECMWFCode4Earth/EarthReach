from enum import Enum


class QualityCriteria(Enum):
    COHERENCE = "coherence"
    FLUENCY = "fluency"
    CONSISTENCY = "consistency"
    RELEVANCE = "relevance"

    @classmethod
    def list(cls) -> list[str]:
        return [criterion.value for criterion in cls]
