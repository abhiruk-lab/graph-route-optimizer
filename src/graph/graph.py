"""Adjacency-list graph representation of the road network.

Adjacency list is used over an adjacency matrix because road networks are
sparse (each intersection connects to a handful of neighbors, not all V
nodes) — this gives O(V + E) space instead of O(V^2).
"""

from collections import defaultdict

from src.graph.edge import Edge
from src.graph.node import Node


class Graph:
    def __init__(self) -> None:
        self._nodes: dict[int, Node] = {}
        self._adjacency: dict[int, list[Edge]] = defaultdict(list)

    def add_node(self, node: Node) -> None:
        self._nodes[node.id] = node

    def add_edge(self, from_id: int, to_id: int, weight: float, bidirectional: bool = False) -> None:
        """Add a directed edge from_id -> to_id.

        Set bidirectional=True for two-way streets (adds the reverse edge too).
        """
        self._adjacency[from_id].append(Edge(to_node=to_id, weight=weight))
        if bidirectional:
            self._adjacency[to_id].append(Edge(to_node=from_id, weight=weight))

    def neighbors(self, node_id: int) -> list[Edge]:
        return self._adjacency[node_id]

    def get_node(self, node_id: int) -> Node:
        return self._nodes[node_id]

    def all_nodes(self) -> list[Node]:
        return list(self._nodes.values())

    def __len__(self) -> int:
        return len(self._nodes)

    # TODO(Phase 1): load_from_osm(path) — build a Graph from an OSM extract
    # (e.g. via osmnx or a raw .osm.pbf parse). Keep this as a classmethod
    # so Graph itself stays data-source-agnostic.
