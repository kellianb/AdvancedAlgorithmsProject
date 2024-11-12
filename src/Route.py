from src.Location import Location
from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class Route:
    """Class for storing data about VRP Routes."""
    warehouse: Location
    customers: list[Location]

    def __init__(self, warehouse: Location, customers: list[Location]):
        self.warehouse = warehouse
        self.customers = customers

    def len(self) -> float:
        lenght = 0
        for i in range(len(self.customers) - 1):
            lenght += self.customers[i].distance_to(self.customers[i+1])

        lenght += self.warehouse.distance_to(self.customers[0])
        lenght += self.customers[-1].distance_to(self.warehouse)

        return lenght
            

    def plot(self, title: str = "Vehicle Route", figsize: tuple = (10, 8)):
        """
        Plot a VRP route showing warehouse, customers, and the complete path.
        
        Args:
            route (Route): Route object containing warehouse and customer locations
            title (str): Title for the plot
            figsize (tuple): Figure size in inches (width, height)
        """
        # Create figure and axis
        fig, ax = plt.subplots(figsize=figsize)
        
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

        len = self.len()
        
        # Add title and total distance
        ax.set_title(f"{title} - Total Distance: {str(len)}")
        
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


