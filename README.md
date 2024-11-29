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

# Project setup steps

## Create venv
```bash
python -m venv ./venv
```

## Activate venv
```bash
# Windows
venv\Scripts\activate.bat

# MacOs/Linux
source myvenv/bin/activate
```

## Install dependencies in venv
```bash
pip install -r requirements.txt
```

# VRP formulation

We have a graph $G = (V, E)$, where :
- $V$ is a set whose elements are called _vertices_ (representing warehouse: $\{V_1\}$ and the customers: $\{V_2,...,V_n\}$), 
- $E$ is a set of unordered pairs $(i, j)$ of vertices and their associated weights, whose elements are called edges
(representing the routes between the vertices). We will consider that our graph is fully connected.

We also define the following variables:

- $n$ : Number of locations (number of elements in $V$)
- $i, j$ : These variables will be used to represent different vertices in $V$
- $w(i, j)$ : Weight of the edge (distance) between vertices $i$ and $j$
- $o(i)$ : Opening time of the delivery window of vertex $i$
- $e(i)$ : Ending time of the delivery window of vertex $i$
- $d_{j}$ : Demand of vertex $j$
- $p$ : Number of trucks in the fleet
- $k$ : This variable will be used to represent different trucks in our fleet
- $Q_k$ : Capacity of the truck $k$
- $t_{ki}$ : Arrival time of truck $k$ at node $i$

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

### Deliveries have to be made during the delivery time window

$s_i + t_{ij} - M \times (1 - x_{ijk}) \leq s_j$
$M = \max \{e_i + t_{ij} - o_j\}$

$o(j) \leq t_{kj} \le e(j)$
$\quad\quad \forall x_{ijk} = 1,$
$\quad\quad i,j \in \{1, ..., n\}$

## Fitness function
$Min\displaystyle\sum_{k=1}^p\sum_{i=1}^n\sum_{i=1}^n w(i,j)x_{ijk}$


# Proof that the VRP is NP-hard
First of all, since the VRP is not a decision problem, but an optimization problem, it cannot be NP-complete.

# Ant Hill Meta-heuristic

## Probability formula
An ant will move from node $i$ to node $j$ with probability :

$p_{i, j}=\frac{\left(\tau_{i, j}^\alpha\right)\left(\eta_{i, j}^\beta\right)}{\sum\left(\tau_{i, j}^\alpha\right)\left(\eta_{i, j}^\beta\right)}$

where
- $\tau_{i, j}$ is the amount of pheromone on edge $i, j$

- $\alpha$ is a parameter to control the influence of $\tau_{i, j}$

- $\eta_{i, j}$ is the desirability of edge $i, j$ (typically $1 / d_{i, j}$ ) 

- $\beta$ is a parameter to control the influence of $\eta_{i, j}$

## Pheromone formula
Amount of pheromone is updated according to the equation

$$
\tau_{i, j}=(1-\rho) \tau_{i, j}+\Delta \tau_{i, j}
$$

where
- $\tau_{i, j}$ is the amount of pheromone on a given edge $i, j$

- $\rho$ is the rate of pheromone evaporation

- $\Delta \tau_{i, j}$ is the amount of pheromone deposited, typically given by:


$$
\Delta \tau_{i, j}^k= \begin{cases}1 / L_k & \text { if ant } k \text { travels on edge } i, j \\ 0 & \text { otherwise }\end{cases}
$$

where 
- $L_k$ is the cost of the $k^{\text {th }}$ ant's tour (typically length).

NOTE: We will have to find a way to include the time window constraint into this


# TODO
- Fix time constraint
- Look into : Local search, Ant colony, Variable neighbourhood search

- Use nearest neighbor first, set all phermones to 1/cost of initial solution
- Use ant colony system
- Only use local search sparingly (only one or two iterations)