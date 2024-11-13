# Introduction
In the **Vehicle Routing Problem (VRP)**, a set number of customers have to be delivered to by a set amount of delivery trucks.

The **VRP** is and extension of the **Traveling Salesman Problem (TSP)** with multiple entities (trucks) making deliveries 
at the same time instead of only one salesman. 
Furthermore, additional restrictions such as delivery time windows or truck capacity are often imposed.

In our case we will impose these restrictions:

- **Vehicle Capacity Constraints:** Each vehicle has a maximum capacity, and the sum of the demands of the customers served on the same route must not exceed this capacity.
- **Service Time Windows:** Each customer has a specific time window during which they must be served. This imposes a restriction on the vehicle’s arrival: it must arrive at the customer within this time frame. If it arrives before the window opens, it must wait; if it arrives after, the route is invalid.
- **Return to Depot Constraint:** Each route must start and end at the central depot, and each vehicle must complete a single trip starting from the depot and return once its route is finished.
- **Single Visit per Customer:** Each customer must be visited exactly once by a vehicle (within the framework of the classic VRPTW).

To simplify, we consider that the travel time (from $i$ to $j$) equals the distance between $i$ and $j$. 

The objective is to minimize the number of routes and the total time/distance traveled by the trucks.

# VRP formulation

We have a graph $G = (V, E)$, where :
- $V$ is a set whose elements are called _vertices_ (representing the customers and warehouse) , 
- $E$ is a set of unordered pairs $(i, j)$ of vertices, whose elements are called edges
(representing the routes between the vertices). We will consider that our graph is fully connected.

We also define the following variables:

- $n$ : Number of customers (number of elements in $V$)
- $i, j$ : These variables will be used to represent different vertices in $V$
- $d_{ij}$ : Distance between vertices $i$ and $j$
- $D_{j}$ : Demand of vertex $j$
- $p$ : Number of trucks in the fleet
- $k$ : This variable will be used to represent different trucks in our fleet
- $c_k$ : Capacity of the truck $k$

## Decision variables
- $x_{ijk}$ : Defines whether the truck $k$ travelling from $i$ to $j$ is part of the solution, allowed values : $\{0, 1\}$. 

## Constraints
- Truck capacity constraint :
$\displaystyle\sum_i^n\sum_j^n x_{ijk} D_j \le c_k \quad \forall k \in \{1, ..., p\}$

-


# Project setup steps

## Create venv
```bash
python -m venv ./venv
```

## Activate venv
```
# Windows
venv\Scripts\activate.bat

# MacOs/Linux
source myvenv/bin/activate
```

## Install dependencies in venv
```
pip install -r requirements.txt
```