from copy import deepcopy
from dataclasses import dataclass
from matplotlib import pyplot as plt
from src.Location import Location
from src.Route import Route
import src.Heuristics.AntColony as AntColony
from typing import Optional


@dataclass
class Vrp:
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

    def nearest_neighbor_heuristic(self) -> "Vrp":
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

    def aco_heuristic(self, n_ants: int, max_iter: int, alpha: int, beta: int, rho: float, plot: bool = False) -> "Vrp":
        """Generate VRP routes using the ACO heuristic
            :param plot: plot the best cost history
            :param n_ants: Number of ants to use
            :param max_iter: Maximum number of iterations
            :param alpha: Alpha parameter, controls the influence of pheromones
            :param beta: Beta parameter, controls the influence of cost
            :param rho: Rho parameter, controls the pheromone evaporation rate
            :param plot: Plot the best cost history
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
        for _ in range(max_iter):
            # Generate solutions concurrently
            solutions = [AntColony.construct_solution(alpha, beta, deepcopy(self._locationBuf), self.warehouse,
                                                      self.vehicleCapacity, pheromones) for _ in range(n_ants)]

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

    def acs_heuristic(self, n_ants: int, max_iter: int, alpha: int, beta: int, rho: float, plot: bool = False) -> "Vrp":
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
        for _ in range(max_iter):
            # Generate solutions concurrently

            solutions = [AntColony.construct_solution(alpha, beta, deepcopy(self._locationBuf), self.warehouse,
                                                      self.vehicleCapacity, pheromones) for _ in range(n_ants)]

            self._acs_heuristic_update_pheromones(solutions, rho, pheromones, deepcopy(self._locationBuf),
                                                  pheromone_val)

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

    def _acs_heuristic_update_pheromones(self, solutions: list[list[Route]], rho: float, pheromones: dict,
                                         customers: list[Location], initial_solution: float):
        """Update the pheromone levels based on the routes taken
            :arg routes: List of routes taken
            :arg rho: Rho parameter, controls the pheromone evaporation rate
            :arg pheromones: Pheromone matrix
        """
        # Evaporate pheromones
        for key in pheromones.keys():
            pheromones[key] = (1 - rho) * pheromones[key] + rho * (1 / len(customers) * initial_solution)

        # Identify the best solution in this iteration
        best_solution = min(solutions, key=lambda sol: self.total_cost(sol))
        best_cost = self.total_cost(best_solution)

        # Intensify pheromones for the best solution
        for route in best_solution:
            # Add pheromones for the edges between the warehouse and the customers in the best solution
            pheromones[(self.warehouse, route.customers[0])] = (1 - rho) * pheromones[
                (self.warehouse, route.customers[0])] + rho / best_cost

            # Add the pheromones for the edges between the customers in the best solution
            for i in range(len(route.customers) - 1):
                pheromones[(route.customers[i], route.customers[i + 1])] = (1 - rho) * pheromones[
                    (route.customers[i], route.customers[i + 1])] + rho / best_cost

            # Add pheromones for the edge between the last customer and the warehouse in the best solution
            pheromones[(route.customers[-1], self.warehouse)] = (1 - rho) * pheromones[
                (route.customers[-1], self.warehouse)] + rho / best_cost

        # Add pheromones to the edges taken
        # for solution in solutions:
        # deposit = 1 / self.total_cost(solution)

        # for route in solution:
        # Add pheromones for the edges between the warehouse and the customers
        # pheromones[(self.warehouse, route.customers[0])] += deposit

        # Add the pheromones for the edges between the customers
        # for i in range(len(route.customers) - 1):
        # pheromones[(route.customers[i], route.customers[i + 1])] += deposit

        # Add pheromones for the edge between the last customer and the warehouse
        # pheromones[(route.customers[-1], self.warehouse)] += deposit

    def total_cost(self, routes: Optional[list[Route]] = None) -> float:
        """Calculate the total cost of all routes
        :arg routes: (Optional) List of routes to calculate the cost for, if left empty, the routes in the iteration are used"""
        routes = routes if routes else self.routes
        return sum([route.cost() for route in routes])

    def print(self, routes: Optional[list[Route]] = None) -> "Vrp":
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

    def cws_heuristic(self) -> "Vrp":
        # Step 1 : Initialize routes
        routes = [Route(warehouse=self.warehouse, customers=[loc]) for loc in
                  self._locationBuf]  # Create a route for each location in the location buffer and add it to the routes list

        # Step 2 : Calculate the savings
        savings = []
        for i in range(len(routes)):
            for j in range(i + 1, len(routes)):  # For each pair of routes
                route_i = routes[i]  # Get the first route
                route_j = routes[j]  # Get the second route
                warehouse = self.warehouse  # Get the warehouse location
                loc_i = route_i.customers[-1]  # Get the last customer of the first route
                loc_j = route_j.customers[0]  # Get the first customer of the second route
                saving = warehouse.distance_to(loc_i) + warehouse.distance_to(loc_j) - loc_i.distance_to(
                    loc_j)  # Calculate the saving
                savings.append((saving, route_i, route_j))  # Add the saving to the list of savings

        # Step 3 : Sort the savings
        savings.sort(reverse=True, key=lambda x: x[0])  # Sort the savings in descending order

        # Step 4 : Merge routes based on savings
        for saving, route_i, route_j in savings:
            if route_i in routes and route_j in routes:
                total_demand = route_i.demand() + route_j.demand()  # Calculate the total demand of the two routes
                if total_demand <= self.vehicleCapacity:  # Check if the total demand is less than or equal to the vehicle capacity
                    merged_route = route_i.merge(route_j)  # Merge the two routes into a single route
                    routes.remove(route_i)
                    routes.remove(route_j)
                    routes.append(merged_route)

        self.routes = routes
        return self

    def plot(self) -> "Vrp":
        for i in range(len(self.routes)):
            self.routes[i].plot(xmin=self._xmin, xmax=self._xmax, ymin=self._ymin, ymax=self._ymax,
                                title=f"Route {i + 1}")
        return self
