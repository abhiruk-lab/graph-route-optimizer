"""CLI entry point.

Usage (point-based — recommended, works for any location):
    python -m src.api.main --center "28.3670,75.5872" --radius 3000 \
        --start "28.3670,75.5872" --end "28.3620,75.5950"

Usage (place-name-based — only works if Nominatim has a polygon boundary
for the place; fails with a TypeError for many small towns/campuses):
    python -m src.api.main --place "Jhunjhunu, Rajasthan, India" \
        --start "28.3670,75.5872" --end "28.3620,75.5950"

First run for a given area will be slow (fetching + building the graph
from OpenStreetMap). osmnx caches the raw HTTP responses to disk by default,
so subsequent runs for the same area are much faster.

TODO(Phase 5): swap this for a REST API (FastAPI/Flask) once the core
algorithms are stable — keep this CLI as a thin wrapper either way, so the
routing logic never depends on the interface layer (this is the Strategy /
separation-of-concerns point to make about the architecture in interviews).
"""

import argparse
import time

from src.algorithms.astar import astar
from src.algorithms.dijkstra import dijkstra
from src.algorithms.heuristics import haversine_distance
from src.graph.graph import Graph
from src.index.kdtree import KDTree


def parse_latlon(s: str) -> tuple[float, float]:
    lat_str, lon_str = s.split(",")
    return float(lat_str), float(lon_str)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute a shortest route between two points.")
    area_group = parser.add_mutually_exclusive_group(required=True)
    area_group.add_argument("--place", help='Geocodable place with a known boundary, e.g. "Jhunjhunu, Rajasthan, India"')
    area_group.add_argument("--center", help='Center coordinate "lat,lon" to fetch a radius around — works for any location')
    parser.add_argument("--radius", type=int, default=3000, help="Radius in meters when using --center (default 3000)")
    parser.add_argument("--start", required=True, help='Start coordinate as "lat,lon"')
    parser.add_argument("--end", required=True, help='End coordinate as "lat,lon"')
    parser.add_argument("--algo", choices=["dijkstra", "astar"], default="astar")
    args = parser.parse_args()

    start_lat, start_lon = parse_latlon(args.start)
    end_lat, end_lon = parse_latlon(args.end)

    print("Loading road network (first run for this area may take a while)...")
    t0 = time.time()
    if args.place:
        graph = Graph.load_from_osm(args.place)
    else:
        center_lat, center_lon = parse_latlon(args.center)
        graph = Graph.load_from_point(center_lat, center_lon, dist=args.radius)
    print(f"Loaded {len(graph)} nodes in {time.time() - t0:.1f}s")

    # Snap the raw start/end coordinates to the nearest actual graph nodes —
    # a user-supplied lat/lon almost never lands exactly on a node.
    index = KDTree(graph.all_nodes())
    start_node = index.nearest(start_lat, start_lon)
    end_node = index.nearest(end_lat, end_lon)
    print(f"Snapped start -> node {start_node.id} ({start_node.lat}, {start_node.lon})")
    print(f"Snapped end   -> node {end_node.id} ({end_node.lat}, {end_node.lon})")

    t0 = time.time()
    if args.algo == "dijkstra":
        cost, path = dijkstra(graph, start_node.id, end_node.id)
    else:
        heuristic = lambda nid, goal_id: haversine_distance(graph.get_node(nid), graph.get_node(goal_id))
        cost, path = astar(graph, start_node.id, end_node.id, heuristic)
    elapsed = time.time() - t0

    print(f"\nAlgorithm: {args.algo}")
    print(f"Distance: {cost:.1f} m")
    print(f"Nodes in path: {len(path)}")
    print(f"Query time: {elapsed * 1000:.2f} ms")


if __name__ == "__main__":
    main()
