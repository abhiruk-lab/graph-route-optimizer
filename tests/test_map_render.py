import os

import pytest

from src.graph.graph import Graph
from src.graph.node import Node
from src.viz.map_render import render_route


def _small_graph() -> Graph:
    g = Graph()
    g.add_node(Node(id=1, lat=28.0, lon=77.0))
    g.add_node(Node(id=2, lat=28.001, lon=77.001))
    g.add_node(Node(id=3, lat=28.002, lon=77.002))
    g.add_edge(1, 2, weight=100.0, bidirectional=True)
    g.add_edge(2, 3, weight=100.0, bidirectional=True)
    return g


def test_render_route_writes_html_file(tmp_path):
    g = _small_graph()
    out = tmp_path / "route.html"
    render_route(g, path=[1, 2, 3], output_path=str(out))

    assert out.exists()
    content = out.read_text()
    # folium output is a full Leaflet-backed HTML doc; sanity check it's
    # non-trivial and actually mentions the map library rather than being
    # an empty/broken file.
    assert "leaflet" in content.lower()
    assert len(content) > 500


def test_render_route_without_network_overlay(tmp_path):
    g = _small_graph()
    out = tmp_path / "route_clean.html"
    render_route(g, path=[1, 2, 3], output_path=str(out), show_full_network=False)
    assert out.exists()


def test_render_route_empty_path_raises(tmp_path):
    g = _small_graph()
    out = tmp_path / "should_not_exist.html"
    with pytest.raises(ValueError):
        render_route(g, path=[], output_path=str(out))
    assert not out.exists()
