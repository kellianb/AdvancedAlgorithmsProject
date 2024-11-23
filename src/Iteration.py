from copy import deepcopy
from dataclasses import dataclass
from matplotlib import pyplot as plt
from src.Location import Location
from src.Route import Route
import src.Heuristics.AntColony as AntColony
from typing import Optional
from multiprocessing import Pool


@dataclass
class Iteration:
    vehicleNumber: int
    vehicleCapacity: int
    warehouse: Location
    routes: list[Route]
    _locationBuf: list[Location]

    # Required for plotting
    _xmin: int
    _ymin: int
    _xmax: int
    _ymax: int

    def __init__(self, warehouse: Location, locations: list[Location], vehicle_number: int, vehicle_capacity: int):
        self._locationBuf = locations
        self.warehouse = warehouse
        self.vehicleNumber = vehicle_number
        self.vehicleCapacity = vehicle_capacity
        self.routes = []
        self._xmin = min([loc.x for loc in self._locationBuf] + [self.warehouse.x]) - 10
        self._ymin = min([loc.y for loc in self._locationBuf] + [self.warehouse.y]) - 10
        self._xmax = max([loc.x for loc in self._locationBuf] + [self.warehouse.x]) + 10
        self._ymax = max([loc.y for loc in self._locationBuf] + [self.warehouse.y]) + 10

    def nearest_neighbor_heuristic(self) -> "Iteration":
        locations = deepcopy(self._locationBuf)
        while locations:
            # Create a new route
            route = Route(warehouse=self.warehouse, customers=[])
            current = self.warehouse

            cost = 0
            demand = 0

            while True:
                current, additional_cost, locations = current.find_nearest_reachable(locations, cost)

                cost += additional_cost

                # If no reachable customer is found
                if not current:
                    break

                demand += current.demand

                # Return if max_demand is reached
                if demand > self.vehicleCapacity:
                    # Add the current location back onto the list of locations
                    locations.append(current)
                    break

                route.customers.append(current)

            # Append the route to the list of routes
            self.routes.append(route)
        return self

    def aco_heuristic(self, n_ants: int, max_iter: int, alpha: int, beta: int, rho: float, plot: bool = False) -> list[
        float]:
        """Generate VRP routes using the ACO heuristic
            :param plot: plot the best cost history
            :param n_ants: Number of ants to use
            :param max_iter: Maximum number of iterations
            :param alpha: Alpha parameter, controls the influence of pheromones
            :param beta: Beta parameter, controls the influence of cost
            :param rho: Rho parameter, controls the pheromone evaporation rate
        """
        # Pheromone matrix : (a : b) -> pheromone level from location a to b
        pheromones = {}
        best_cost = float("inf")
        best_solution = None
        best_cost_history = []

        # Initialize pheromones
        # Uses the result of a past heuristic as a starting point if available
        pheromone_val = 1 / self.total_cost() if self.routes else 1

        for a in self._locationBuf + [self.warehouse]:
            for b in self._locationBuf + [self.warehouse]:
                if b != a:
                    pheromones[(a, b)] = pheromone_val

        # Run max_iter iterations
        with Pool() as pool:
            for _ in range(max_iter):
                # Generate solutions concurrently
                solutions = pool.starmap(AntColony.construct_solution, [
                    (alpha, beta, deepcopy(self._locationBuf), self.warehouse, self.vehicleCapacity, pheromones) for _
                    in range(n_ants)])

                self._aco_heuristic_update_pheromones(solutions, rho, pheromones)

                # Find the best solution
                for solution in solutions:
                    cost = self.total_cost(solution)

                    if cost < best_cost:
                        best_cost = cost
                        best_solution = solution

                best_cost_history.append(best_cost)

        if plot:
            plt.plot(range(len(best_cost_history)), best_cost_history)
            plt.title('Best cost history')

        self.routes = best_solution

        return self

    def _aco_heuristic_update_pheromones(self, solutions: list[list[Route]], rho: float, pheromones: dict):
        """Update the pheromone levels based on the routes taken
            :arg routes: List of routes taken
            :arg rho: Rho parameter, controls the pheromone evaporation rate
            :arg pheromones: Pheromone matrix
        """
        # Evaporate pheromones
        for key in pheromones.keys():
            pheromones[key] *= (1 - rho)

        # Add pheromones to the edges taken
        for solution in solutions:
            deposit = 1 / self.total_cost(solution)

            for route in solution:
                # Add pheromones for the edges between the warehouse and the customers
                pheromones[(self.warehouse, route.customers[0])] += deposit

                # Add the pheromones for the edges between the customers
                for i in range(len(route.customers) - 1):
                    pheromones[(route.customers[i], route.customers[i + 1])] += deposit

                # Add pheromones for the edge between the last customer and the warehouse
                pheromones[(route.customers[-1], self.warehouse)] += deposit

    def total_cost(self, routes: Optional[list[Route]] = None) -> float:
        """Calculate the total cost of all routes
        :arg routes: (Optional) List of routes to calculate the cost for, if left empty, the routes in the iteration are used"""
        routes = routes if routes else self.routes
        return sum([route.cost() for route in routes])

    def print(self, routes: Optional[list[Route]] = None) -> "Iteration":
        """Print the details of the iteration"""
        routes = routes if routes else self.routes
        print("==== Iteration =====")
        print(f"Total cost: {self.total_cost(routes)}")
        print(f"Total routes: {len(routes)}")
        print("\n")
        for i, route in enumerate(routes):
            route.print(name=f"Route {i + 1}")
            print("")
        return self

    def plot(self) -> "Iteration":
        for i in range(len(self.routes)):
            self.routes[i].plot(xmin=self._xmin, xmax=self._xmax, ymin=self._ymin, ymax=self._ymax,
                                title=f"Route {i + 1}")
        return self
