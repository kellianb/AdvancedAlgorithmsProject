from operator import itemgetter
from typing import Optional

from src.Location import Location
from dataclasses import dataclass
import matplotlib.pyplot as plt
import itertools


@dataclass
class Route:
    """Class for storing data about VRP Routes."""
    warehouse: Location
    customers: list[Location]

    def __init__(self, warehouse: Location, customers: list[Location]):
        self.warehouse = warehouse
        self.customers = customers

    def len(self) -> float:
        """Calculate total route distance"""
        length = self.warehouse.distance_to(self.customers[0])

        for i in range(len(self.customers) - 1):
            length += self.customers[i].distance_to(self.customers[i + 1])

        length += self.customers[-1].distance_to(self.warehouse)

        return length

    def merge(self, other: "Route") -> "Route":
        """Merge another route into the current one"""
        self.customers += other.customers
        return self

    def demand(self) -> int:
        """Get total demand of all customers in the route"""
        return sum([customer.demand for customer in self.customers])

    def cost(self) -> float:
        """Calculate total cost (distance and possible waiting time for package readiness)"""

        cost = self.warehouse.distance_to(self.customers[0])

        for i in range(len(self.customers) - 1):
            # If the truck arrives before the package is ready, it must wait
            # Since distance = time in our model, we add the waiting time to the cost

            cost += max(self.customers[i].ready_time - cost, 0)

            # Add the travel distance to the next customer to the cost
            cost += self.customers[i].distance_to(self.customers[i + 1])

        cost += self.customers[-1].distance_to(self.warehouse)

        return cost

    # Route solvers
    def brute_force(self):
        """Brute force the route, this does not take into account the delivery windows"""
        permutations = [Route(self.warehouse, list(record)) for record in itertools.permutations(self.customers)]
        lens = [(record.len(), record) for record in permutations]

        return min(lens, key=itemgetter(0))[1]

    def nearest_neighbour(self) -> "Route":
        """Solve the route with the nearest neighbour algorithm"""
        route = Route(warehouse=self.warehouse, customers=[])

        locations = self.customers.copy()

        current = locations.pop(0)

        while locations:
            current, locations = current.find_closest(locations)
            route.customers.append(current)

        return route

    def plot(self, xmin=Optional[int], xmax=Optional[int], ymin=Optional[int], ymax=Optional[int],
             title: str = "Vehicle Route", figsize: tuple = (10, 8)):
        """
        Plot a VRP route showing warehouse, customers, and the complete path.
        
        Args:
            route (Route): Route object containing warehouse and customer locations
            title (str): Title for the plot
            figsize (tuple): Figure size in inches (width, height)
            :param figsize: figsize
            :param title: Title of the plot
            :param ymax: Max y of the plot
            :param ymin: Min y of the plot
            :param xmax: Max x of the plot
            :param xmin: Min x of the plot
        """
        # Create figure and axis
        fig, ax = plt.subplots(figsize=figsize)

        if xmin and xmax and ymin and ymax:
            ax.set_xlim(left=xmin, right=xmax)
            ax.set_ylim(bottom=ymin, top=ymax)

        # Plot warehouse
        ax.scatter(self.warehouse.x, self.warehouse.y,
                   c='red', s=100, label='Warehouse',
                   marker='s', zorder=3)

        # Plot customers
        ax.scatter([c.x for c in self.customers], [c.y for c in self.customers],
                   c='blue', s=80, label='Customers',
                   marker='o', zorder=2)

        # Create route path including return to warehouse
        path_x = [self.warehouse.x] + [c.x for c in self.customers] + [self.warehouse.x]
        path_y = [self.warehouse.y] + [c.y for c in self.customers] + [self.warehouse.y]

        # Plot route path
        ax.plot(path_x, path_y, 'g--', alpha=0.7,
                linewidth=1.5, label='Route', zorder=1)

        # Add labels for warehouse and customers
        ax.annotate('W', (self.warehouse.x, self.warehouse.y),
                    xytext=(5, 5), textcoords='offset points')

        for loc in self.customers:
            ax.annotate(f'C{loc.id}', (loc.x, loc.y),
                        xytext=(5, 5), textcoords='offset points')

        # Add title and total distance
        ax.set_title(f"{title}")

        infostr = f"Distance: {str(self.len())}"
        infostr += f"\nCost: {str(self.cost())}"
        infostr += f"\nDemand: {str(self.demand())}"
        infostr += f"\nCustomer No: {len(self.customers)}"

        plt.figtext(0.68, 0.15, infostr)

        # Add legend
        ax.legend()

        # Equal aspect ratio for proper distance visualization
        ax.set_aspect('equal')

        # Add grid
        ax.grid(True, linestyle=':', alpha=0.6)

        # Add labels
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')

        plt.grid(True, linestyle='--', alpha=0.7)

        # Auto-adjust margins
        plt.tight_layout()

        return fig, ax
