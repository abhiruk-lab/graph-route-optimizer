"""Represents a single point in the road network (an intersection/junction)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    """A graph node corresponding to a real-world location.

    Attributes:
        id: Unique identifier (e.g. OSM node id).
        lat: Latitude in decimal degrees.
        lon: Longitude in decimal degrees.
    """
    id: int
    lat: float
    lon: float

    def as_tuple(self) -> tuple[float, float]:
        """Return (lat, lon) — convenient for spatial index insertion."""
        return (self.lat, self.lon)
