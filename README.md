# Advanced Algorithms Project - Group 3
- Kellian Bechtel 
- Guillaume Ferrand
- Emma Grummann
- Maxime Haas

# Introduction
In the **Vehicle Routing Problem with Time Windows (VRPTW)**, a set number of customers have to be delivered to by a set amount of delivery trucks.

The **VRPTW** is and extension of the **Traveling Salesman Problem (TSP)** with multiple entities (trucks) making deliveries 
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

# VRPTW formulation

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
- $s_{i}$ : service time of vertex $i$
- $p$ : Number of trucks in the fleet
- $k$ : This variable will be used to represent different trucks in our fleet
- $Q_k$ : Capacity of the truck $k$
- $t_{ki}$ : Arrival time of truck $k$ at vertex $i$ (value defined in the section "Deliveries have to be made during the delivery time window")

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

$t_{ki} + s_i + w(i, j) - M \times (1 - x_{ijk}) \leq t_{kj}$
$\quad\quad \forall i \in V \quad j \in V \text{ \ } \{1\}  \quad k \in \{1, ..., p\} $

$o(i) \le t_{ki} \le e(i) $
$\quad\quad \forall i \in V \quad k \in \{1, ..., p\} $


$M = \max \{ e(i) + s_i + w(i, j) - o(j) \}$

## Fitness function
$Min\displaystyle\sum_{k=1}^p\sum_{i=1}^n\sum_{i=1}^n w(i,j)x_{ijk}$


# Complexity class of VRPTW
VRPTW is a combinatorial optimization problem that falls within the complexity class NP-Complete.

In this section, we will prove that VRPTW is in NP and NP-Complete.

## VRPTW is in NP

To prove VRPTW is in NP, we show that any certificate to the problem can be verified in polynomial time. 
The decision problem is: 

*Given a VRPTW $G$ and a certificate $s$, is $s$ an admissible solution to $G$?*

### Certificate
The VRPTW certificate is a set of routes, each of which is an ordered list of nodes $v \in V$.

**Example :** $\text{Route 1} : 1 \rightarrow 2 \rightarrow 3 \rightarrow 4 \rightarrow 1 $ 
(Where node $1$ is the depot and nodes $2$, $3$ and $4$ are customers)

### Verification Process
   - **Capacity Check**: Ensure the total demand of all customers on each route does not exceed the vehicle's capacity $Q_k$. This step takes $O(|V|)$ time for each route.
   - **Customer Visit Check**: Ensure every customer $v \in V \setminus \{v_0\}$ is visited exactly once across all routes. This can be verified in $O(|V|)$ time by marking nodes as visited.
   - **Cost Calculation**: Sum the total cost (distance + service time + waiting time) $c_{ij}$ for all edges in the routes and check if it matches the given solution cost. This step takes $O(|E|)$ time, as each edge is processed once.

### Polynomial Time 
Since all verification steps (capacity check, visit check, and cost calculation) can be performed in polynomial time relative to the size of the input, VRPTW is in NP.

### Conclusion 
A solution of VRPTW can be verified in polynomial time, so **VRPTW is in NP**.


## VRPTW is NP-Complete

To prove VRPTW is NP-Complete, we will reduce a known NP-complete problem (TSP) to VRPTW in polynomial time.

### TSP Definition
TSP is defined on a graph $G = (V, E)$ with a cost matrix $C = [c_{ij}]$. 
The objective is to find a minimum-cost Hamiltonian circuit that visits each node exactly once and returns to the starting node.

### VRPTW Reducibility to TSP

The Vehicle Routing Problem (VRP) can be reduced to the Traveling Salesman Problem with time windows (TSP) in polynomial time, proving that VRPTW shares the same complexity class as TSP, which is NP-complete.

| **TSP**                          | **VRPTW**                                    |
|:---------------------------------|----------------------------------------------|
| One traveller                    | Several vehicles                             |
| Unlimited capacity (single trip) | Truck capacity (multiple trips may be needed) |
| No time restrictions             | Time slots for each delivery point           |
| No capcity restrictions          | Each truck has a set capacity                |


### Mapping TSP to VRPTW
Given an instance of TSP, we construct an equivalent instance of VRPTW:
- Set the number of vehicles to $p = 1$.
- Set the vehicle capacity $Q_k$ to a sufficiently large value so that a single vehicle can serve all customers (i.e., $\displaystyle Q \geq \sum^{v \in V} d(v)$).
- Assign demand $d(v) = 1$ for each customer $v \in V$, ensuring the vehicle can transport all packages in a single trip.
- Set the depot as any node $v_0 \in V$.
- Set the service time of each customer to $0$.
- Set the delivery time window for each customer to $[0, \infty[$, allowing the vehicle to visit any customer at any time.

TSP can therefore be reduced to VRPTW.

## Conclusion
VRPTW is in NP and a known NP-Complete problem is reductible to VRPTW, proving that the VRPTW is in the NP-Complete complexity class.


# Ant Hill Meta-heuristic

### Probability formula
An ant will move from node $i$ to node $j$ with probability :

$p_{i, j}=\frac{\left(\tau_{i, j}^\alpha\right)\left(\eta_{i, j}^\beta\right)}{\sum\left(\tau_{i, j}^\alpha\right)\left(\eta_{i, j}^\beta\right)}$

where
- $\tau_{i, j}$ is the amount of pheromone on edge $i, j$

- $\alpha$ is a parameter to control the influence of $\tau_{i, j}$

- $\eta_{i, j}$ is the desirability of edge $i, j$ (typically $1 / d_{i, j}$ ) 

- $\beta$ is a parameter to control the influence of $\eta_{i, j}$

### Pheromone formula
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
- $L_k$ is the total cost of the $k^{\text {th }}$ ant's tour (distance + service time + waiting time).