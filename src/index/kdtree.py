"""KD-tree spatial index for O(log V) nearest-node queries.

Used to answer "which graph node is closest to this arbitrary lat/lon?" —
needed whenever a route request starts from a raw GPS coordinate rather
than an existing node id. Naive linear scan is O(V); a balanced KD-tree
brings this down to O(log V) on average.
"""

from src.graph.node import Node


class KDNode:
    def __init__(self, point: Node, left: "KDNode | None" = None, right: "KDNode | None" = None):
        self.point = point
        self.left = left
        self.right = right


class KDTree:
    def __init__(self, points: list[Node]):
        self.root = self._build(points, depth=0)

    def _build(self, points: list[Node], depth: int) -> KDNode | None:
        if not points:
            return None

        axis = depth % 2  # alternate lat / lon
        points.sort(key=lambda n: n.lat if axis == 0 else n.lon)
        median = len(points) // 2

        return KDNode(
            point=points[median],
            left=self._build(points[:median], depth + 1),
            right=self._build(points[median + 1:], depth + 1),
        )

    def nearest(self, lat: float, lon: float) -> Node:
        """Return the Node closest to (lat, lon)."""
        best = self._nearest(self.root, lat, lon, depth=0, best=None)
        return best.point

    def _nearest(self, node: KDNode | None, lat: float, lon: float, depth: int, best: KDNode | None) -> KDNode:
        if node is None:
            return best

        if best is None or self._dist_sq(node.point, lat, lon) < self._dist_sq(best.point, lat, lon):
            best = node

        axis = depth % 2
        query_val = lat if axis == 0 else lon
        node_val = node.point.lat if axis == 0 else node.point.lon

        near_branch, far_branch = (node.left, node.right) if query_val < node_val else (node.right, node.left)

        best = self._nearest(near_branch, lat, lon, depth + 1, best)

        # Only check the far branch if it could plausibly contain a closer point.
        if (query_val - node_val) ** 2 < self._dist_sq(best.point, lat, lon):
            best = self._nearest(far_branch, lat, lon, depth + 1, best)

        return best

    @staticmethod
    def _dist_sq(point: Node, lat: float, lon: float) -> float:
        return (point.lat - lat) ** 2 + (point.lon - lon) ** 2

# TODO(Phase 3): benchmark against a naive O(V) linear scan to quantify
# the speedup on the real dataset — this is the number to put in the README.
