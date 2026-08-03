"""Render a computed route on a map.

Planned approach (Phase 6): use folium (Leaflet.js wrapper) to plot the
path's node coordinates as a polyline over an OpenStreetMap base layer,
and export to HTML for the README GIF/screenshot.
"""

from src.graph.graph import Graph


def render_route(graph: Graph, path: list[int], output_path: str = "route.html") -> None:
    """Render `path` (a list of node ids) as a line on a map, saved to output_path.

    TODO(Phase 6): implement with folium:
        import folium
        coords = [(graph.get_node(nid).lat, graph.get_node(nid).lon) for nid in path]
        m = folium.Map(location=coords[0], zoom_start=13)
        folium.PolyLine(coords, weight=5).add_to(m)
        m.save(output_path)
    """
    raise NotImplementedError("Implement in Phase 6 with folium or matplotlib + basemap.")
