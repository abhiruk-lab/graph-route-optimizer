"""Represents a directed connection between two nodes."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
    """A directed, weighted edge in the road network.

    Attributes:
        to_node: id of the destination Node.
        weight: Edge weight (distance in meters by default; could represent
            time or cost if a different weight function is plugged in).
    """
    to_node: int
    weight: float
