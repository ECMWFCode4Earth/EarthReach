"""
Pressure-Center Data Extractor module.

This module provides functionality to extract pressure centers (high and low pressure systems)
from meteorological data, specifically mean sea level pressure fields in GRIB format.
It uses simple local extrema detection to identify these centers.
"""

from dataclasses import dataclass
from typing import Any

import earthkit.data as ekd
import numpy as np

from scipy.ndimage import maximum_filter, minimum_filter

from earth_reach.config.logging import get_logger
from earth_reach.core.extractors.base_extractor import BaseDataExtractor

logger = get_logger(__name__)


@dataclass
class PressureCenter:
    """Data structure for a pressure center."""

    center_type: str
    latitude: float
    longitude: float
    center_value_hPa: float
    grid_indices: tuple[int, int]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "center_type": self.center_type,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "center_value_hPa": self.center_value_hPa,
            "grid_indices": self.grid_indices,
        }


class PressureCenterDataExtractor(BaseDataExtractor):
    """
    Concrete implementation for extracting pressure centers from GRIB data.

    Uses local extrema detection to identify high and low pressure centers
    in mean sea level pressure fields.
    """

    def __init__(
        self,
        pressure_var_name: str = "msl",
        neighborhood_size: int = 200,
    ):
        """
        Initialize the pressure center extractor.

        Args:
            pressure_var_name: Name of pressure variable in GRIB data
            neighborhood_size: Size of neighborhood for local extrema detection
        """

        self.neighborhood_size = neighborhood_size
        self.pressure_var_name = pressure_var_name

    def validate_data(
        self, data: ekd.FieldList
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Validate and return GRIB data pressure field.

        Args:
            data (ekd.FieldList): GRIB data to validate

        Returns:
            Tuple of (data array, latitudes, longitudes)

        Raises:
            ValueError: If required pressure variable not found
        """
        try:
            available_vars = [str(var) for var in data.metadata("shortName")]
            if self.pressure_var_name not in available_vars:
                raise ValueError(
                    f"Required variable '{self.pressure_var_name}' not found. "
                    f"Available variables: {', '.join(available_vars)}",
                )

            data_field = data.sel(shortName=self.pressure_var_name)[0]
            if not isinstance(data_field, ekd.Field):
                raise ValueError(
                    "Could not extract a valid pressure field from data.",
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
            logger.error("Pressure centers data extractor validation failed: %s", e)
            raise

    def extract(
        self,
        data: ekd.FieldList,
        **kwargs: Any,
    ) -> list[PressureCenter]:
        """
        Extract pressure centers from GRIB data.

        Args:
            data (ekd.FieldList): Input GRIB data
            **kwargs: Additional extraction parameters

        Returns:
            List[PressureCenter]: List of PressureCenter objects
        """
        pressure_centers = []
        try:
            data_arr, lats, lons = self.validate_data(data)
            local_min = data == minimum_filter(data_arr, size=self.neighborhood_size)
            local_max = data == maximum_filter(data_arr, size=self.neighborhood_size)

            if local_max is None or local_min is None:
                raise ValueError(
                    "Could not find local extrema in the data.",
                )

            min_indices = np.where(local_min)
            max_indices = np.where(local_max)
            for i in range(len(min_indices[0])):
                row, col = min_indices[0][i], min_indices[1][i]
                pressure_centers.append(
                    PressureCenter(
                        center_type="low",
                        latitude=lats[row, col],
                        longitude=lons[row, col],
                        center_value_hPa=data_arr[row, col],
                        grid_indices=(row, col),
                    ),
                )
            for i in range(len(max_indices[0])):
                row, col = max_indices[0][i], max_indices[1][i]
                pressure_centers.append(
                    PressureCenter(
                        center_type="high",
                        latitude=lats[row, col],
                        longitude=lons[row, col],
                        center_value_hPa=data_arr[row, col],
                        grid_indices=(row, col),
                    ),
                )

            return pressure_centers
        except Exception as e:
            logger.error("Pressure center data extraction failed: %s", e)
            return []

    def format_features_to_str(self, features: list[PressureCenter]) -> str:
        """Format extracted temperature features into a prompt-friendly string."""

        output_str = "## Presure Center Extractor Output\n\n"
        if not features:
            output_str += "No pressure centers could be extracted.\n"
            return output_str

        low_pressure_centers = sorted(
            [center for center in features if center.center_type == "low"],
            key=lambda x: x.center_value_hPa,
        )
        high_pressure_centers = sorted(
            [center for center in features if center.center_type == "high"],
            key=lambda x: x.center_value_hPa,
            reverse=True,
        )
        output_str += "**Low Pressure Centers**:\n"
        for center in low_pressure_centers:
            output_str += (
                f"- {center.center_type.capitalize()} pressure center at "
                f"({center.latitude:.2f}°N, {center.longitude:.2f}°E) "
                f"with value {center.center_value_hPa:.2f} hPa.\n"
            )
        output_str += "\n**High Pressure Centers**:\n"
        for center in high_pressure_centers:
            output_str += (
                f"- {center.center_type.capitalize()} pressure center at "
                f"({center.latitude:.2f}°N, {center.longitude:.2f}°E) "
                f"with value {center.center_value_hPa:.2f} hPa.\n"
            )

        return output_str
