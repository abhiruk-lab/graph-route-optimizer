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

    @classmethod
    def load_from_osm(cls, place_name: str, network_type: str = "drive") -> "Graph":
        """Build a Graph from a real-world OSM road network, by place name.

        Args:
            place_name: A geocodable place query, e.g. "Jhunjhunu, Rajasthan, India".
            network_type: osmnx network filter — "drive" excludes footpaths/
                cycleways so the graph only contains roads a vehicle can use.

        Requires Nominatim to have an administrative *polygon* boundary for
        the query — this fails with a TypeError for places Nominatim only
        knows as a single point (many smaller towns, campuses, villages).
        For those, use load_from_point instead, which needs only a center
        coordinate and a radius rather than a named boundary.
        """
        import osmnx as ox

        osm_graph = ox.graph_from_place(place_name, network_type=network_type)
        return cls._from_osmnx_graph(osm_graph)

    @classmethod
    def load_from_point(cls, lat: float, lon: float, dist: int = 3000, network_type: str = "drive") -> "Graph":
        """Build a Graph from OSM data within `dist` meters of (lat, lon).

        More robust than load_from_osm for places without a Nominatim
        polygon boundary (small towns, campuses, villages) — only needs a
        center point, not a named/geocoded area.

        Args:
            lat, lon: Center coordinate.
            dist: Radius in meters to pull road network data for. Larger
                values mean more nodes/edges and a slower fetch — 2000-5000m
                is a reasonable range for a first working demo.
            network_type: osmnx network filter — "drive" excludes footpaths/
                cycleways so the graph only contains roads a vehicle can use.
        """
        import osmnx as ox

        osm_graph = ox.graph_from_point((lat, lon), dist=dist, network_type=network_type)
        return cls._from_osmnx_graph(osm_graph)

    @staticmethod
    def _from_osmnx_graph(osm_graph) -> "Graph":
        """Shared conversion: an osmnx-returned networkx MultiDiGraph -> our Graph.

        osmnx graphs are already directed (one-way streets are represented
        correctly) with node attributes 'y' (lat) / 'x' (lon) and edge
        attribute 'length' (meters). We map that directly onto our own
        Node/Edge representation rather than depending on networkx's graph
        API elsewhere in the codebase — this keeps osmnx/networkx as a
        data-loading detail, not a core dependency the algorithms rely on.
        """
        graph = Graph()

        for node_id, data in osm_graph.nodes(data=True):
            graph.add_node(Node(id=node_id, lat=data["y"], lon=data["x"]))

        for u, v, data in osm_graph.edges(data=True):
            # A MultiDiGraph can have multiple parallel edges between the
            # same u, v (e.g. divided roads modeled as two ways) — we keep
            # them all rather than collapsing to one, since Dijkstra/A* just
            # pick the cheapest path through whichever edges exist; extra
            # parallel edges never produce an incorrect result, only
            # (harmlessly) redundant ones.
            weight = data.get("length", 0.0)
            graph.add_edge(u, v, weight=weight)

        return graph
