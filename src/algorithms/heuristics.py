"""Heuristic functions for A* search.

A heuristic must be admissible (never overestimates true cost) for A* to
stay optimal. Great-circle (haversine) distance is admissible for road
networks because actual road distance is always >= straight-line distance.
"""

import math

from src.graph.node import Node

EARTH_RADIUS_M = 6_371_000


def haversine_distance(a: Node, b: Node) -> float:
    """Great-circle distance between two lat/lon points, in meters."""
    lat1, lon1 = math.radians(a.lat), math.radians(a.lon)
    lat2, lon2 = math.radians(b.lat), math.radians(b.lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    h = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(h))
