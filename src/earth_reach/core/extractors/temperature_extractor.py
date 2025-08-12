"""
Temperature Data Extractor module.

This module provides functionality to extract temperature data
from meteorological datasets, specifically 2-meter temperature fields in GRIB format.
It includes data validation and formatting for prompt updates.
"""

from dataclasses import dataclass
from typing import Any

import earthkit.data as ekd
import numpy as np
import xarray as xr

from earth_reach.config.logging import get_logger
from earth_reach.core.extractors.base_extractor import BaseDataExtractor
from earth_reach.core.utils import get_root_dir_path

logger = get_logger(__name__)


@dataclass
class TemperatureData:
    """Data structure for temperature data."""

    domain: str
    month: str
    temperature_C: float
    average_temperature_C: float
    latitude: float
    longitude: float
    grid_indices: tuple[int, int]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "domain": self.domain,
            "month": self.month,
            "temperature_C": self.temperature_C,
            "average_temperature_C": self.average_temperature_C,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "grid_indices": self.grid_indices,
        }


class TemperatureDataExtractor(BaseDataExtractor):
    """Concrete implementation for extracting temperature data from GRIB data."""

    def __init__(self, temperature_var_name: str = "2t"):
        """
        Initialize the temperature data extractor.

        Args:
            temperature_var_name (str): Name of the temperature variable in GRIB data.
        """
        self.temperature_var_name = temperature_var_name
        self.average_temp_data = xr.open_dataset(
            get_root_dir_path() / "data" / "average_monthly_regional_temperature.nc"
        )

    def validate_data(self, data: ekd.FieldList) -> ekd.FieldList:
        """
        Parse, validate and return GRIB data.

        Args:
            data (ekd.FieldList): Input data to validate

        Returns:
            ekd.FieldList: Parsed and validated data

        Raises:
            ValueError: If validation fails
        """
        try:
            available_vars = [str(var) for var in data.metadata("shortName")]
            if self.temperature_var_name not in available_vars:
                raise ValueError(
                    f"Required variable '{self.temperature_var_name}' not found. "
                    f"Available variables: {', '.join(available_vars)}",
                )

            data_field = data.sel(shortName=self.temperature_var_name)[0]
            if not isinstance(data_field, ekd.Field):
                raise ValueError(
                    "Could not extract a valid temperature field from data.",
                )
            data_arr = data_field.to_numpy()
            if data_arr is None or not isinstance(data_arr, np.ndarray):
                raise ValueError("Data array is empty or not a valid numpy array.")

            latlons = data_field.to_latlon()
            lats = latlons["lat"]
            lons = latlons["lon"]

            if lats is None or lons is None:
                raise ValueError("Could not extract latitude/longitude coordinates")

            logger.info("Validation passed.")
            return data_arr, lats, lons
        except ValueError as e:
            logger.error(f"Validation failed: {e!s}")
            raise

    def extract(self, data: ekd.FieldList, **kwargs: Any) -> list[TemperatureData]:
        """
        Extract temperature features from the input data.

        Args:
            data (ekd.FieldList): Input data
            **kwargs: Additional extraction parameters

        Returns:
            List[TemperatureData]: List of extracted temperature features
        """
        temperature_data = []
        try:
            temperature_arr, lats, lons = self.validate_data(data)
            # 0. Possible to split in sub-regions ? Should extract regions around hotest / coldest points ?
            # 1. Get domain and month from kwargs
            # 2. If domain or month is not provided, try to infer from field
            # 3. Convert domain to longitude and latitude bounds
            # 4. Compute average temperature for the domain and month on field data
            # 5. Compare with average temperature from precomputed data, assume normal distribution
            #    to find anomalies according to std deviation or z-score
            # 6. Build TemperatureData object
            return temperature_data
        except IndexError as e:
            raise ValueError(
                f"Temperature variable '{self.temperature_var_name}' not found in data"
            ) from e

    def format_features_to_str(self, features: list[TemperatureData]) -> str:
        """Format extracted temperature features into a prompt-friendly string."""
