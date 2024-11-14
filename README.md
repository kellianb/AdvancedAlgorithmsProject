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
- $V$ is a set whose elements are called _vertices_ (representing warehouse: $\{V_1\}$ and the customers: $\{V_2,...,V_n\}$), 
- $E$ is a set of unordered pairs $(i, j)$ of vertices and their associated weights, whose elements are called edges
(representing the routes between the vertices). We will consider that our graph is fully connected.

We also define the following variables:

- $n$ : Number of locations (number of elements in $V$)
- $i, j$ : These variables will be used to represent different vertices in $V$
- $w(i, j)$ : Weight of the edge (distance) between vertices $i$ and $j$
- $d_{j}$ : Demand of vertex $j$
- $p$ : Number of trucks in the fleet
- $k$ : This variable will be used to represent different trucks in our fleet
- $Q_k$ : Capacity of the truck $k$

## Decision variables
- $x_{ijk}$ : Defines whether the truck $k$ travelling from $i$ to $j$ is part of the solution.

```math
x_{ijk} = \begin{cases} 1 & \text{if truck } k \text{ goes from vertex } i \text{ to vertex } j \\ 0 & \text{otherwise} \end{cases}
```


## Constraints
### All customers are visited exactly once

  $\displaystyle\sum_{k=1}^p\sum_{i=1}^n x_{ijk} =1$
  $\quad\quad \forall j \in \{2, ..., n\},$ 
  $\quad i \in \{1, ..., n \},$
  $\quad k \in \{1, ..., p\}$
 
### Trucks leaves node as often as it enters

  $\displaystyle\sum_{i=1}^n x_{ijk} = \sum_{i=1}^n x_{jik}$
  $\quad\quad \forall j \in \{1, ..., n\},$
  $\quad i \in \{1, ..., n \},$
  $\quad k \in \{1, ..., p\}$


### Truck capacity constraint
  
  $\displaystyle\sum_{i=1}^n\sum_{j=1}^n x_{ijk} d_j \le Q_k$ 
  $\quad\quad \forall k \in \{1, ..., p\},$
  $\quad i,j \in \{1, ..., n\}$

### All trucks leave the depot

  $\displaystyle\sum_{j=2}^n x_{1jk} = 1$
  $\quad\quad \forall k \in \{1, ..., p\},$
  $\quad j \in \{2, ..., n \}$



# Proof that the VRP is NP-hard
First of all, since the VRP is not a decision problem, but an optimization problem, it cannot be NP-complete.


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