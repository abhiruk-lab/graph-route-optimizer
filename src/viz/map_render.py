"""Render a computed route on a map.

Uses folium (a thin Python wrapper around Leaflet.js) to plot the route as
a polyline over an OpenStreetMap base layer, with start/end markers, and
exports to a standalone HTML file you can open in a browser or embed in
the README.
"""

from src.graph.graph import Graph


def render_route(
    graph: Graph,
    path: list[int],
    output_path: str = "route.html",
    show_full_network: bool = True,
) -> None:
    """Render `path` (a list of node ids) as a line on a map, saved to output_path.

    Args:
        graph: The full loaded road network (used for context and, if
            show_full_network=True, to draw every edge faintly in the
            background so the route's context is visible).
        path: Ordered list of node ids forming the route, e.g. the `path`
            returned by dijkstra()/astar().
        output_path: Where to write the standalone HTML file.
        show_full_network: If True, draw all graph edges as thin grey lines
            behind the highlighted route — useful for seeing how the route
            was chosen relative to the surrounding street grid. Set False
            for a cleaner image on dense networks where this gets noisy.

    Raises:
        ValueError: if path is empty (nothing to render).
    """
    import folium

    if not path:
        raise ValueError("Cannot render an empty path.")

    route_coords = [(graph.get_node(nid).lat, graph.get_node(nid).lon) for nid in path]

    # Center the map on the route's midpoint rather than its first node, so
    # short routes near the edge of the fetched area still frame nicely.
    mid = route_coords[len(route_coords) // 2]
    m = folium.Map(location=mid, zoom_start=15, tiles="cartodbpositron")

    if show_full_network:
        for node in graph.all_nodes():
            for edge in graph.neighbors(node.id):
                neighbor = graph.get_node(edge.to_node)
                folium.PolyLine(
                    [(node.lat, node.lon), (neighbor.lat, neighbor.lon)],
                    color="#999999",
                    weight=1,
                    opacity=0.4,
                ).add_to(m)

    folium.PolyLine(route_coords, color="#e6194b", weight=5, opacity=0.9).add_to(m)

    start, end = route_coords[0], route_coords[-1]
    folium.Marker(start, tooltip="Start", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(end, tooltip="End", icon=folium.Icon(color="red")).add_to(m)

    m.save(output_path)
