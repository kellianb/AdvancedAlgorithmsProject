from typing import Optional
from src.Route import Route
from src.Location import Location
import numpy as np
import random


def construct_solution(
    alpha: int,
    beta: int,
    customers: list[Location],
    warehouse: Location,
    vehicle_capacity: int,
    pheromones: dict,
) -> list[Route]:
    solution = []
    unvisited = customers
    random.shuffle(unvisited)
    # Generate vehicle routes
    while unvisited:
        new_route = Route(warehouse, [])

        total_route_demand = 0
        current = warehouse
        current_cost = 0

        # Assign customers to vehicles
        while total_route_demand < vehicle_capacity:
            next_loc = _select_next_location(
                current,
                unvisited,
                current_cost,
                vehicle_capacity - total_route_demand,
                alpha,
                beta,
                pheromones,
            )

            if not next_loc:
                break

            new_route.customers.append(next_loc)
            total_route_demand += next_loc.demand
            current_cost = current.cost_to(next_loc, current_cost)
            unvisited.remove(next_loc)
            current = next_loc

        solution.append(new_route)

    return solution


def _select_next_location(
    current: Location,
    unvisited: list[Location],
    current_cost: int,
    capacity: int,
    alpha: int,
    beta: int,
    pheromones: dict,
) -> Optional[Location]:
    """Select the next location for the ACO heuristic
    :arg current: Current location
    :arg unvisited: List of unvisited locations
    :arg current_cost: Cost already incurred on this route
    :arg capacity: Remaining capacity of the vehicle
    :arg alpha: Alpha parameter, controls the influence of pheromones
    :arg beta: Beta parameter, controls the influence of cost
    :arg pheromones: Pheromone matrix
    """
    probabilities = {}
    reachable_delivery_windows = current.find_deliverable(
        unvisited, capacity, current_cost
    )

    reachable_delivery_windows.sort(key=lambda c: (c.due_date, -c.demand))

    # If no reachable delivery windows are found
    if not reachable_delivery_windows:
        return None

    # Calculate the probabilities of selecting each location
    for next_loc in reachable_delivery_windows:
        # Amount of pheromone on the edge between the current location and next_loc
        pheromone = pheromones[(current, next_loc)]

        # Cost to deliver to next_loc
        cost = current.distance_to(next_loc)

        # Desirability of next_loc
        desirability = 1 / (cost + 1e-9)

        probabilities[next_loc] = (pheromone**alpha) * (desirability**beta)

    # Normalize the probabilities
    total = sum(probabilities.values())
    probabilities = {loc: prob / (total) for loc, prob in probabilities.items()}

    return np.random.choice(list(probabilities.keys()), p=list(probabilities.values()))
