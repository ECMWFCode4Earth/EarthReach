"""
Base Data Extractor module.

This module defines the abstract base class for data extractors in the EarthReach project.
It provides a common interface and functionality for extracting meteorological features
from GRIB files.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseDataExtractor(ABC):
    """
    Abstract base class for weather data extractors.

    Provides common functionality and interface for extracting
    meteorological features from various data sources.
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize the data extractor.

        Args:
            verbose: Whether to print progress messages
        """
        self.verbose = verbose
        self._data = None
        self._metadata = {}

    @abstractmethod
    def validate_data(self, data: Any) -> bool:
        """
        Validate that the input data contains required variables.

        Args:
            data: Input data to validate

        Returns:
            bool: True if validation passes

        Raises:
            ValueError: If validation fails
        """

    @abstractmethod
    def extract(self, data: Any, **kwargs) -> list[Any]:
        """
        Extract features from the input data.

        Args:
            data: Input data
            **kwargs: Additional extraction parameters

        Returns:
            List of extracted features
        """

    @abstractmethod
    def add_data_to_prompt(self, prompt: str, features: list[Any]) -> str:
        """
        Format data and add them to the prompt.

        Args:
            prompt: Prompt string to modify
            features: List of extracted features

        Returns:
            str: Updated prompt with formatted data
        """
