"""
Base Data Extractor module.

This module defines the abstract base class for data extractors.
It provides a common interface and functionality for extracting meteorological features
from GRIB files.
"""

from abc import ABC, abstractmethod
from typing import Any

import earthkit.data as ekd


class BaseDataExtractor(ABC):
    """Abstract base class for weather data extractors."""

    @abstractmethod
    def validate_data(self, data: ekd.FieldList) -> Any:
        """
        Parse, validate and return GRIB data.

        Args:
            data (ekd.FieldList): Input data to validate

        Returns:
            Any: Parsed and validated data

        Raises:
            ValueError: If validation fails
        """

    @abstractmethod
    def extract(self, data: ekd.FieldList, **kwargs: Any) -> list[Any]:
        """
        Extract features from the input data.

        Args:
            data: Input data
            **kwargs: Additional extraction parameters

        Returns:
            List of extracted features
        """

    @abstractmethod
    def format_features_to_str(self, features: list[Any]) -> str:
        """
        Format extracted features into a prompt-friendly string.

        Args:
            features: List of extracted features

        Returns:
            str: Formatted string for prompt update
        """
