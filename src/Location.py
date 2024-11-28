from copy import deepcopy
from math import sqrt
from dataclasses import dataclass
from operator import itemgetter
from typing import Optional


@dataclass(frozen=True)
class Location:
    """Class for storing data about VRP locations."""
    id: int
    x: int
    y: int
    demand: int
    ready_time: int
    due_date: int
    service: int

    def distance_to(self, other: "Location") -> float:
        """Calculate the distance to travel from the current location to another location.
            :arg other: The other location to calculate the distance to"""
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def cost_to(self, other: "Location", current_cost: float = 0) -> float:
        """Calculate the cost to travel from the current location to another location and add the waiting time at the target location.
            :param current_cost: The cost that was already incurred before reaching this location
            :arg other: The other location to calculate the cost to"""
        current_cost += self.distance_to(other)

        # Add potential waiting time
        current_cost += max(other.ready_time - current_cost, 0)

        # Add service time
        current_cost += other.service
        return current_cost

    def find_reachable(self, others: list["Location"], current_cost: int = 0) -> list["Location"]:
        """Find all neighbors whose delivery windows are reachable from the current location, return them.
            :arg others: list of locations to check
            :arg current_cost: Cost that was already incurred before reaching this location
            :return List of reachable locations
        """
        return [loc for loc in deepcopy(others) if loc.due_date >= self.distance_to(loc) + current_cost]

    def find_deliverable(self, others: list["Location"], capacity: int, current_cost: int = 0) -> list["Location"]:
        """Find all neighbors whose delivery windows are reachable from the current location and whose demand can be fulfilled with the remaining truck capacity, return them.
            :arg others: list of locations to check
            :arg capacity: Available truck capacity
            :arg current_cost: Cost that was already incurred before reaching this location
            :return List of deliverable locations
        """
        return [loc for loc in self.find_reachable(others, current_cost) if loc.demand <= capacity]

    def find_closest(self, others: list["Location"]) -> tuple["Location", list["Location"]]:
        """Find the closest neighbor to the current location in a list, return it and the remaining list.
            :arg others: list of locations to check
        """
        closest = min(others, key=lambda x: self.distance_to(x))

        others.remove(closest)

        return closest, others

    def find_nearest_reachable(self, others: list["Location"], current_cost: int = 0) -> tuple[
        Optional["Location"], float, list["Location"]]:
        """Then find the neighbor that is the cheapest to deliver to from the current location, return it and the remaining list.

            If no suitable neighbor is found, return None.

            :arg others: list of locations to check
            :arg current_cost: Cost that was already incurred before reaching this location
            :return: Closest neighbor to the current location, The Cost to get to this neighbor and the remaining list.
            """

        # Remove elements that cannot be reached
        others_reachable = self.find_reachable(others, current_cost)

        if not others_reachable:
            return None, current_cost, others

        cheapest = min(others_reachable, key=lambda x: self.cost_to(x, current_cost))

        others.remove(cheapest)

        return cheapest, self.cost_to(cheapest, current_cost), others
