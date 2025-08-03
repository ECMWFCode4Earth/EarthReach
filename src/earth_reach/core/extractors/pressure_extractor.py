"""
Pressure-Center Data Extractor module.

This module provides functionality to extract pressure centers (high and low pressure systems)
from meteorological data, specifically mean sea level pressure fields in GRIB format.
It uses local extrema detection with Gaussian smoothing to identify these centers.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import numpy as np

from scipy.ndimage import gaussian_filter, maximum_filter, minimum_filter

from earth_reach.config.logging import get_logger
from earth_reach.core.extractors.base_extractor import BaseDataExtractor

logger = get_logger(__name__)


@dataclass
class PressureCenter:
    """Data structure for a pressure center."""

    center_type: str
    latitude: float
    longitude: float
    pressure_hPa: float
    intensity: float
    timestamp: datetime
    confidence: float
    grid_indices: tuple[int, int]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "type": self.center_type,
            "lat": self.latitude,
            "lon": self.longitude,
            "pressure_hPa": self.pressure_hPa,
            "intensity": self.intensity,
            "timestamp": self.timestamp.isoformat(),
            "confidence": self.confidence,
            "grid_indices": self.grid_indices,
        }


class PressureCenterDataExtractor(BaseDataExtractor):
    """
    Concrete implementation for extracting pressure centers from GRIB data.

    Uses local extrema detection with Gaussian smoothing to identify
    high and low pressure centers in mean sea level pressure fields.
    """

    def __init__(
        self,
        sigma: float = 1.0,
        min_distance: float = 500.0,  # km
        min_intensity: float = 1.0,  # hPa
        neighborhood: int = 8,  # 4 or 8 connected
        pressure_var_name: str = "msl",
        **kwargs,
    ):
        """
        Initialize the pressure center extractor.

        Args:
            sigma: Gaussian smoothing parameter (grid points)
            min_distance: Minimum distance between centers (km)
            min_intensity: Minimum pressure difference to be considered a center (hPa)
            neighborhood: 4 or 8 connected neighborhood for extrema detection
            pressure_var_name: Name of pressure variable in GRIB data
            **kwargs: Additional arguments passed to parent class
        """
        super().__init__(**kwargs)

        self.sigma = sigma
        self.min_distance = min_distance
        self.min_intensity = min_intensity
        self.neighborhood = neighborhood
        self.pressure_var_name = pressure_var_name

        if neighborhood not in [4, 8]:
            raise ValueError("neighborhood must be 4 or 8")

    def validate_data(self, data: Any) -> bool:
        """
        Validate GRIB data contains mean sea level pressure.

        Args:
            data: earthkit-data GRIB dataset

        Returns:
            bool: True if validation passes

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

            lats = data.to_numpy(latitude=True)
            lons = data.to_numpy(longitude=True)

            if lats is None or lons is None:
                raise ValueError("Could not extract latitude/longitude coordinates")

            logger.info(f"Validation passed. Found {self.pressure_var_name} variable.")
            return True

        except Exception as e:
            logger.error(f"Validation failed: {e!s}")
            raise

    def extract(
        self,
        data: Any,
        smoothing: bool = True,
        return_all: bool = False,
    ) -> list[PressureCenter]:
        """
        Extract pressure centers from GRIB data.

        Args:
            data: earthkit-data GRIB dataset
            smoothing: Whether to apply Gaussian smoothing
            return_all: If True, return all extrema without filtering

        Returns:
            List of PressureCenter objects
        """
        self.validate_data(data)

        pressure_data = data.sel(shortName=self.pressure_var_name)
        pressure_array = pressure_data.to_numpy()

        lats = pressure_data.to_numpy(latitude=True)
        lons = pressure_data.to_numpy(longitude=True)

        if smoothing and self.sigma > 0:
            pressure_smoothed = gaussian_filter(pressure_array, sigma=self.sigma)
            logger.info(f"Applied Gaussian smoothing with sigma={self.sigma}")
        else:
            pressure_smoothed = pressure_array.copy()

        timestamp = data.datetime()

        high_centers = self._find_extrema(
            pressure_smoothed,
            lats,
            lons,
            timestamp,
            extrema_type="high",
        )
        low_centers = self._find_extrema(
            pressure_smoothed,
            lats,
            lons,
            timestamp,
            extrema_type="low",
        )

        all_centers = high_centers + low_centers

        if return_all:
            return all_centers

        filtered_centers = [c for c in all_centers if c.intensity >= self.min_intensity]

        final_centers = self._filter_by_distance(filtered_centers, lats, lons)

        logger.info(
            f"Extracted {len(final_centers)} pressure centers "
            f"({sum(1 for c in final_centers if c.center_type == 'high')} high, "
            f"{sum(1 for c in final_centers if c.center_type == 'low')} low)",
        )

        return final_centers

    def _find_extrema(
        self,
        pressure: np.ndarray,
        lats: np.ndarray,
        lons: np.ndarray,
        timestamp: datetime,
        extrema_type: str,
    ) -> list[PressureCenter]:
        """Find local extrema in pressure field."""

        if self.neighborhood == 4:
            struct = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        else:  # 8-connected
            struct = np.ones((3, 3))

        if extrema_type == "high":
            extrema = pressure == maximum_filter(pressure, footprint=struct)
        else:  # low
            extrema = pressure == minimum_filter(pressure, footprint=struct)

        extrema[0, :] = False
        extrema[-1, :] = False
        extrema[:, 0] = False
        extrema[:, -1] = False

        centers = []
        indices = np.where(extrema)

        for i, j in zip(indices[0], indices[1], strict=False):
            local_region = pressure[
                max(0, i - 2) : min(pressure.shape[0], i + 3),
                max(0, j - 2) : min(pressure.shape[1], j + 3),
            ]

            if extrema_type == "high":
                intensity = pressure[i, j] - np.mean(
                    local_region[local_region != pressure[i, j]],
                )
            else:
                intensity = (
                    np.mean(local_region[local_region != pressure[i, j]])
                    - pressure[i, j]
                )

            grad_y, grad_x = np.gradient(
                pressure[
                    max(0, i - 1) : min(pressure.shape[0], i + 2),
                    max(0, j - 1) : min(pressure.shape[1], j + 2),
                ],
            )
            gradient_magnitude = np.sqrt(grad_y**2 + grad_x**2).mean()
            confidence = 1.0 - np.exp(-gradient_magnitude)

            center = PressureCenter(
                center_type=extrema_type,
                latitude=float(lats[i, j]) if lats.ndim > 1 else float(lats[i]),
                longitude=float(lons[i, j]) if lons.ndim > 1 else float(lons[j]),
                pressure_hPa=float(pressure[i, j]),
                intensity=abs(float(intensity)),
                timestamp=timestamp,
                confidence=float(confidence),
                grid_indices=(int(i), int(j)),
            )
            centers.append(center)

        return centers

    def _filter_by_distance(
        self,
        centers: list[PressureCenter],
        lats: np.ndarray,
        lons: np.ndarray,
    ) -> list[PressureCenter]:
        """Filter centers to ensure minimum distance between them."""

        if not centers or self.min_distance <= 0:
            return centers

        sorted_centers = sorted(centers, key=lambda c: c.intensity, reverse=True)

        kept_centers = []
        for center in sorted_centers:
            too_close = False
            for kept in kept_centers:
                distance = self._haversine_distance(
                    center.latitude,
                    center.longitude,
                    kept.latitude,
                    kept.longitude,
                )
                if distance < self.min_distance:
                    too_close = True
                    break

            if not too_close:
                kept_centers.append(center)

        return kept_centers

    def _haversine_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
    ) -> float:
        """Calculate distance between two points on Earth (km)."""
        R = 6371  # Earth radius in km

        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(a))

        return R * c

    def format_output(self, prompt: str, features: list[PressureCenter]) -> str:
        raise NotImplementedError(
            "Should implement this method before use with DataExtractor",
        )
