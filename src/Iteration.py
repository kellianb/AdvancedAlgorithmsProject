from dataclasses import dataclass
from src.Location import Location
from src.Route import Route


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
        while self._locationBuf:
            route = Route(warehouse=self.warehouse, customers=self._locationBuf)
            new_route, self._locationBuf = route.nearest_neighbour_heuristic(self.vehicleCapacity)
            self.routes.append(new_route)

        return self

    def plot(self) -> "Iteration":
        for i in range(len(self.routes)):
            self.routes[i].plot(xmin=self._xmin, xmax=self._xmax, ymin=self._ymin, ymax=self._ymax,
                                title=f"Route {i + 1}")
        return self
