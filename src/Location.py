from copy import deepcopy
from math import sqrt
from dataclasses import dataclass
from operator import itemgetter
from typing import Optional


@dataclass
class Location:
    """Class for storing data about VRP locations."""
    id: int
    x: int
    y: int
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
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def cost_to(self, other: "Location", current_cost: int = 0) -> float:
        current_cost += self.distance_to(other)

        # Add potential waiting time
        current_cost += max(other.ready_time - current_cost, 0)
        return current_cost

    def find_closest(self, others: list["Location"]) -> tuple["Location", list["Location"]]:
        """Find the closest neighbor to the current location in a list, return it and the remaining list.
            :arg others: list of locations to check
        """
        distance_pairs = [(self.distance_to(record), record) for record in others]

        # Sort by distance
        distance_pairs.sort(key=itemgetter(0))

        # First element is closest
        closest = distance_pairs.pop(0)[1]

        # Rest are the remaining locations
        others = [pair[1] for pair in distance_pairs]

        return closest, others

    def find_nearest_reachable(self, others: list["Location"], current_cost: int = 0) -> tuple[
        Optional["Location"], float, list["Location"]]:
        """Then find the neighbor that is the cheapest to deliver to from the current location, return it and the remaining list.

            If no neighbor is found, return None.

            :arg others: list of locations to check
            :arg current_cost: Cost that was already incurred before reaching this location
            :return: Closest neighbor to the current location, The Cost to get to this neighbor and the remaining list.
            """

        # Remove elements that cannot be reached
        others_reachable = [loc for loc in deepcopy(others) if loc.due_date >= self.distance_to(loc) + current_cost]

        if not others_reachable:
            return None, current_cost, others

        cheapest = min(others_reachable, key=lambda x: self.cost_to(x, current_cost))

        others.remove(cheapest)

        return cheapest, self.cost_to(cheapest, current_cost), others
