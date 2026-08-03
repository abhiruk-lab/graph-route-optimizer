from src.graph.graph import Graph
from src.graph.node import Node


def test_add_node_and_get_node():
    g = Graph()
    n = Node(id=1, lat=28.0, lon=77.0)
    g.add_node(n)
    assert g.get_node(1) == n


def test_add_edge_directed():
    g = Graph()
    g.add_edge(1, 2, weight=5.0)
    neighbors = g.neighbors(1)
    assert len(neighbors) == 1
    assert neighbors[0].to_node == 2
    assert neighbors[0].weight == 5.0
    # Directed: no reverse edge should exist.
    assert g.neighbors(2) == []


def test_add_edge_bidirectional():
    g = Graph()
    g.add_edge(1, 2, weight=5.0, bidirectional=True)
    assert g.neighbors(1)[0].to_node == 2
    assert g.neighbors(2)[0].to_node == 1


def test_len():
    g = Graph()
    g.add_node(Node(id=1, lat=0.0, lon=0.0))
    g.add_node(Node(id=2, lat=1.0, lon=1.0))
    assert len(g) == 2
