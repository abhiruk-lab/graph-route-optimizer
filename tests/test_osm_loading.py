"""Tests for Graph.load_from_osm.

These tests never touch the network. Instead they monkeypatch
osmnx.graph_from_place to return a small synthetic networkx.MultiDiGraph
built with the exact same shape osmnx produces (node attrs 'y'/'x', edge
attr 'length') — so we're testing our own conversion logic, not osmnx
itself or network availability. This keeps the test suite fast and
runnable in CI/offline.
"""

import networkx as nx
import pytest

osmnx = pytest.importorskip("osmnx")

from src.algorithms.dijkstra import dijkstra
from src.graph.graph import Graph


def _fake_osm_graph() -> nx.MultiDiGraph:
    g = nx.MultiDiGraph()
    g.add_node(101, y=28.3670, x=75.5872)
    g.add_node(102, y=28.3680, x=75.5880)
    g.add_node(103, y=28.3690, x=75.5890)
    g.add_edge(101, 102, length=150.0)
    g.add_edge(102, 103, length=200.0)
    g.add_edge(101, 103, length=500.0)  # longer direct alternative
    return g


def test_load_from_osm_builds_correct_graph(monkeypatch):
    monkeypatch.setattr(osmnx, "graph_from_place", lambda place, network_type="drive": _fake_osm_graph())

    graph = Graph.load_from_osm("fake place")

    assert len(graph) == 3
    node = graph.get_node(101)
    assert node.lat == 28.3670
    assert node.lon == 75.5872


def test_load_from_point_builds_correct_graph(monkeypatch):
    monkeypatch.setattr(osmnx, "graph_from_point", lambda center, dist=3000, network_type="drive": _fake_osm_graph())

    graph = Graph.load_from_point(28.367, 75.587, dist=2000)

    assert len(graph) == 3
    node = graph.get_node(101)
    assert node.lat == 28.3670
    assert node.lon == 75.5872


def test_load_from_osm_shortest_path_prefers_two_hop_route(monkeypatch):
    monkeypatch.setattr(osmnx, "graph_from_place", lambda place, network_type="drive": _fake_osm_graph())

    graph = Graph.load_from_osm("fake place")
    cost, path = dijkstra(graph, 101, 103)

    # 150 + 200 = 350, cheaper than the direct 500m edge.
    assert cost == 350.0
    assert path == [101, 102, 103]
