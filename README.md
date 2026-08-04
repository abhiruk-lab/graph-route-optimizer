# Graph-Based Route Optimization Engine

> A route optimization engine built over real-world road network data — implementing classical and heuristic shortest-path algorithms with spatial indexing for scale.

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-13%20passing-brightgreen)

## Demo

A route computed between two points in Pilani, Rajasthan, rendered over the real OpenStreetMap street grid:

`[Insert screenshot of route.html here — e.g. drag the file into the GitHub README editor, or run: python -m src.api.main --center "28.3670,75.6020" --radius 3000 --start "28.3670,75.6020" --end "28.3620,75.6100" --render route.html, open it in a browser, and screenshot it]`

## Overview

This engine computes shortest paths between arbitrary coordinates over a real road network extracted from OpenStreetMap. It implements Dijkstra's algorithm and A* search from scratch (no reliance on networkx's built-in pathfinding), backed by a custom KD-tree spatial index so arbitrary GPS coordinates can be snapped to the nearest road-network node in O(log n) instead of a linear scan over every node.

**Problem scope:** single-source, single-destination shortest path on a static (non-time-dependent) weighted road graph, where edge weights represent real-world distance in meters. Multi-stop/TSP-style routing is out of scope for this phase (see Limitations).

## Features

- [x] Graph construction from real-world OSM road network data (via osmnx), including a point-radius fallback (`load_from_point`) for locations without a Nominatim administrative boundary polygon
- [x] Dijkstra's shortest-path algorithm (binary min-heap priority queue)
- [x] A* search with an admissible haversine-distance heuristic
- [x] KD-tree spatial index for O(log n) nearest-node queries
- [x] CLI interface
- [x] Map-based route visualization (folium)
- [ ] REST API interface *(stretch)*
- [ ] Multi-stop routing via nearest-neighbor / 2-opt heuristic *(stretch)*
- [ ] Full benchmark suite across multiple graph sizes *(stretch — one comparison run documented below)*

## Architecture

```
data/            # Raw and processed OSM extracts (gitignored cache excluded)
src/
  graph/         # Node, Edge, Graph classes — adjacency list representation
  algorithms/    # Dijkstra, A*, haversine heuristic
  index/         # KD-tree spatial index for nearest-node lookup
  api/           # CLI entry point (src/api/main.py)
  viz/           # folium-based map rendering
tests/           # Unit + integration tests, including OSM-shaped synthetic
                 # graphs so correctness is verified offline/in CI without
                 # depending on a live network call to OpenStreetMap
```

Algorithms are implemented as standalone functions operating on the same `Graph` interface, so switching between Dijkstra and A* is a one-flag change (`--algo dijkstra` / `--algo astar`) with no changes needed to the graph, loading, or CLI layers.

## Benchmarks

Measured on a live OSM extract of Pilani, Rajasthan (1099 nodes, ~3000m radius), computing the shortest path between two points ~950m apart as the crow flies:

| Metric | Dijkstra | A* |
|---|---|---|
| Distance (identical path found) | 1241.6 m | 1241.6 m |
| Nodes in path | 17 | 17 |
| Query time | 0.31 ms | 0.15 ms |

A* returned the exact same optimal cost as Dijkstra (confirming the haversine heuristic is admissible) while running roughly 2x faster by using the heuristic to prioritize search toward the goal instead of expanding uniformly outward.

## Getting Started

### Prerequisites
Python 3.11+, pip

### Installation
```bash
git clone https://github.com/abhiruk-lab/graph-route-optimizer.git
cd graph-route-optimizer
pip install -r requirements.txt
```

### Usage
```bash
# Route by center point + radius (works for any location, including small towns
# without a Nominatim administrative boundary)
python -m src.api.main --center "28.3670,75.6020" --radius 3000 \
    --start "28.3670,75.6020" --end "28.3620,75.6100" --algo astar

# Route by named place (works for larger cities with a known boundary polygon)
python -m src.api.main --place "Jaipur, Rajasthan, India" \
    --start "26.9124,75.7873" --end "26.8850,75.8090"

# Save an interactive HTML map of the computed route
python -m src.api.main --center "28.3670,75.6020" --radius 3000 \
    --start "28.3670,75.6020" --end "28.3620,75.6100" --render route.html
```

### Running tests
```bash
pytest tests/ -v
```
13 tests covering graph construction, Dijkstra/A* correctness, OSM data conversion (against synthetic osmnx-shaped graphs, so no live network call is needed for CI), and map rendering.

## Data Source

Road network data extracted from [OpenStreetMap](https://www.openstreetmap.org/) via [osmnx](https://osmnx.readthedocs.io/), using either `graph_from_place` (named locations with a known administrative boundary) or `graph_from_point` (center coordinate + radius, used as the default/fallback — necessary for smaller towns like Pilani that exist in OSM as a point rather than a bounded polygon).

## Limitations

- **Static graph only** — no live traffic, road closures, or time-dependent weights.
- **No multi-stop/TSP routing** — this engine solves point-to-point shortest path only; visiting an ordered or unordered set of multiple stops (delivery-routing style) is out of scope.
- **Undirected turn restrictions not modeled** — edge weights are purely distance-based; real-world turn restrictions, one-way streets are inherited from OSM's own directed graph representation but no additional turn-penalty logic is applied.
- **`graph_from_place` requires a Nominatim boundary polygon** — smaller towns without one must use `--center`/`--radius` instead; this is handled via a fallback path, not automatically detected/switched.
- **Benchmarks are from a single graph/query pair** — solid enough to demonstrate correctness (A* matches Dijkstra) and relative performance, but not a statistically rigorous sweep across graph sizes.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
