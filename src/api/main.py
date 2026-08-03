"""CLI entry point.

Usage:
    python -m src.api.main --start "28.6139,77.2090" --end "28.7041,77.1025"

TODO(Phase 5): swap this for a REST API (FastAPI/Flask) once the core
algorithms are stable — keep this CLI as a thin wrapper either way, so the
routing logic never depends on the interface layer (this is the Strategy /
separation-of-concerns point to make about the architecture in interviews).
"""

import argparse

from src.algorithms.astar import astar
from src.algorithms.dijkstra import dijkstra
from src.algorithms.heuristics import haversine_distance
from src.graph.graph import Graph


def parse_latlon(s: str) -> tuple[float, float]:
    lat_str, lon_str = s.split(",")
    return float(lat_str), float(lon_str)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute a shortest route between two points.")
    parser.add_argument("--start", required=True, help='Start coordinate as "lat,lon"')
    parser.add_argument("--end", required=True, help='End coordinate as "lat,lon"')
    parser.add_argument("--algo", choices=["dijkstra", "astar"], default="astar")
    args = parser.parse_args()

    start_lat, start_lon = parse_latlon(args.start)
    end_lat, end_lon = parse_latlon(args.end)

    # TODO(Phase 1): load a real graph here (Graph.load_from_osm(...)) and
    # use the KDTree to snap (start_lat, start_lon) / (end_lat, end_lon) to
    # the nearest graph node ids before calling the algorithm below.
    graph = Graph()

    raise NotImplementedError(
        "Wire up graph loading (Phase 1) and node snapping (Phase 3) before running this."
    )


if __name__ == "__main__":
    main()
