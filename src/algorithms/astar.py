"""A* search — Dijkstra's algorithm guided by a heuristic.

Expands fewer nodes than Dijkstra in the common case because the heuristic
biases the search toward the goal, while preserving Dijkstra's optimality
guarantee as long as the heuristic is admissible and consistent.
"""

import heapq
from typing import Callable

from src.graph.graph import Graph


def astar(
    graph: Graph,
    start_id: int,
    end_id: int,
    heuristic: Callable[[int, int], float],
) -> tuple[float, list[int]]:
    """Return (total_distance, path_as_list_of_node_ids).

    `heuristic(node_id, end_id)` should return an admissible estimate of the
    remaining distance to the goal (e.g. haversine_distance).
    """
    g_score: dict[int, float] = {start_id: 0.0}
    previous: dict[int, int] = {}
    visited: set[int] = set()

    # heap entries: (f_score, node_id) where f_score = g_score + heuristic
    heap: list[tuple[float, int]] = [(heuristic(start_id, end_id), start_id)]

    while heap:
        _, current_id = heapq.heappop(heap)

        if current_id in visited:
            continue
        visited.add(current_id)

        if current_id == end_id:
            break

        for edge in graph.neighbors(current_id):
            neighbor_id = edge.to_node
            if neighbor_id in visited:
                continue

            tentative_g = g_score[current_id] + edge.weight
            if tentative_g < g_score.get(neighbor_id, float("inf")):
                g_score[neighbor_id] = tentative_g
                previous[neighbor_id] = current_id
                f_score = tentative_g + heuristic(neighbor_id, end_id)
                heapq.heappush(heap, (f_score, neighbor_id))

    if end_id not in g_score:
        raise ValueError(f"No path found from {start_id} to {end_id}")

    path = [end_id]
    while path[-1] != start_id:
        path.append(previous[path[-1]])
    path.reverse()

    return g_score[end_id], path


# TODO(Phase 2): add node-expansion counter, same as dijkstra.py, for the
# head-to-head benchmark in Phase 6.
