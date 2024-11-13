from math import sqrt
from dataclasses import dataclass
from operator import itemgetter

@dataclass
class Location:
    """Class for storing data about VRP locations."""
    id: int
    x: int
    y:  int
    demand: int
    ready_time: int
    due_date: int
    service: int

    def __init__(self, id: int, x: int, y: int, demand: int, ready_time: int, due_date: int, service: int):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.ready_time = ready_time
        self.due_date = due_date
        self.service = service

    def distance_to(self, other: "Location") -> float:
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def find_closest(self, others: list["Location"]) -> tuple["Location", list["Location"]]:
        """Find the closest location in a list to this location"""
        distance_pairs = [(self.distance_to(record), record) for record in others]

        # Sort by distance
        distance_pairs.sort(key=itemgetter(0))

        # First element is closest
        closest = distance_pairs.pop(0)[1]

        # Rest are the remaining locations
        others = [pair[1] for pair in distance_pairs]

        return closest, others