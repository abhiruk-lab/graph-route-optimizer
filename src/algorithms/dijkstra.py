"""Dijkstra's single-source shortest path algorithm.

Correctness relies on the cut property: at each step, the unvisited node
with the smallest tentative distance has already found its true shortest
path, because all edge weights are non-negative (no shorter path could be
found through a longer-distance node later).

Uses a binary min-heap as the priority queue -> O((V + E) log V).
"""

import heapq

from src.graph.graph import Graph


def dijkstra(graph: Graph, start_id: int, end_id: int) -> tuple[float, list[int]]:
    """Return (total_distance, path_as_list_of_node_ids).

    Raises ValueError if no path exists.
    """
    distances: dict[int, float] = {start_id: 0.0}
    previous: dict[int, int] = {}
    visited: set[int] = set()

    heap: list[tuple[float, int]] = [(0.0, start_id)]

    while heap:
        current_dist, current_id = heapq.heappop(heap)

        if current_id in visited:
            continue
        visited.add(current_id)

        if current_id == end_id:
            break

        for edge in graph.neighbors(current_id):
            neighbor_id = edge.to_node
            if neighbor_id in visited:
                continue

            new_dist = current_dist + edge.weight
            if new_dist < distances.get(neighbor_id, float("inf")):
                distances[neighbor_id] = new_dist
                previous[neighbor_id] = current_id
                heapq.heappush(heap, (new_dist, neighbor_id))

    if end_id not in distances:
        raise ValueError(f"No path found from {start_id} to {end_id}")

    # Reconstruct path by walking `previous` backwards from end to start.
    path = [end_id]
    while path[-1] != start_id:
        path.append(previous[path[-1]])
    path.reverse()

    return distances[end_id], path


# TODO(Phase 2): add node-expansion counter (return it alongside the result)
# so it can be compared directly against A* in the benchmark suite.
