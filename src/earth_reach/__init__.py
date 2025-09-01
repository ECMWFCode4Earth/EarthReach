"""
Main package.

Dual-LLM framework for generating natural language descriptions of meteorological
data visualizations, making weather charts accessible to blind and low-vision scientists.
"""

from earth_reach.core.evaluator import EvaluatorAgent
from earth_reach.core.generator import GeneratorAgent
from earth_reach.core.llm import GeminiLLM, GroqLLM, OpenAILLM
from earth_reach.core.orchestrator import Orchestrator
from earth_reach.main import EarthReachAgent

__all__ = [
    "EarthReachAgent",
    "EvaluatorAgent",
    "GeminiLLM",
    "GeneratorAgent",
    "GroqLLM",
    "OpenAILLM",
    "Orchestrator",
]
