from enum import Enum
from typing import List


class QualityCriteria(Enum):
    COHERENCE = "coherence"
    FLUENCY = "fluency"
    CONSISTENCY = "consistency"
    RELEVANCE = "relevance"

    @classmethod
    def list(cls) -> List[str]:
        return [criterion.value for criterion in cls]
