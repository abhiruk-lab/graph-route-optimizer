import pytest

from src.algorithms.dijkstra import dijkstra
from src.graph.graph import Graph


def build_small_graph() -> Graph:
    """A hand-computable 5-node graph, so shortest paths can be verified by
    inspection rather than trusting the implementation to grade itself.

        1 --2--> 2 --2--> 4
        |               ^
        5               1
        v               |
        3 -------4------ (to 4)
        Shortest 1->4 should be via 2->4: cost 4 (2+2).
    """
    g = Graph()
    for node_id in [1, 2, 3, 4]:
        from src.graph.node import Node
        g.add_node(Node(id=node_id, lat=0.0, lon=0.0))

    g.add_edge(1, 2, weight=2.0)
    g.add_edge(2, 4, weight=2.0)
    g.add_edge(1, 3, weight=5.0)
    g.add_edge(3, 4, weight=4.0)

    return g


def test_dijkstra_shortest_path_cost():
    g = build_small_graph()
    cost, path = dijkstra(g, start_id=1, end_id=4)
    assert cost == 4.0
    assert path == [1, 2, 4]


def test_dijkstra_no_path_raises():
    g = Graph()
    from src.graph.node import Node
    g.add_node(Node(id=1, lat=0.0, lon=0.0))
    g.add_node(Node(id=2, lat=0.0, lon=0.0))
    # No edges added -> unreachable.
    with pytest.raises(ValueError):
        dijkstra(g, start_id=1, end_id=2)


def test_dijkstra_trivial_same_node():
    g = build_small_graph()
    cost, path = dijkstra(g, start_id=1, end_id=1)
    assert cost == 0.0
    assert path == [1]
