# Genetic Algorithm TSP

This project contains a modular and optimized implementation of a **Genetic Algorithm (GA)** designed to solve and visualize the **Traveling Salesperson Problem (TSP)** from scratch. This project was developed as part of the *Computational Intelligence* course.

## Problem Description

The Traveling Salesperson Problem (TSP) is a well-known NP-hard combinatorial optimization problem. Given a set of $N$ cities with 2D coordinates $(x, y)$, the objective is to find the shortest possible route (tour) that visits each city exactly once and returns to the origin city. Since the search space grows factorially ($\frac{1}{2}(N-1)!$), metaheuristic approaches like Genetic Algorithms are ideal for finding optimal or near-optimal solutions.

## Features & Implementation Details

### 1. Mathematical Modeling
- **Distance Matrix:** An $N \times N$ matrix calculated using the Euclidean distance formula between all pairs of cities.
- **Chromosome Representation:** Modeled as a permutation of integers from $1$ to $N$, ensuring no city is duplicated or missed.
- **Fitness Function:** Designed to maximize the inverse of the total tour length ($L$) to favor shorter paths: $$Fitness = \frac{1}{L}$$

### 2. Evolutionary Operators
To avoid generating invalid offspring with duplicate cities, specialized operators have been implemented from scratch:
- **Initial Population:** Generated randomly using diverse permutations of cities.
- **Selection:** Tournament Selection.
- **Crossover:** Order Crossover (OX) to preserve sequence without duplication.
- **Mutation:** Inversion Mutation.

### 3. Visualization
The project utilizes libraries like `matplotlib` to provide clear graphical insights:
- **Convergence Plot:** Displays the evolution of the best (shortest) distance discovered across generations.
- **Graphical Tour:** Plots the input cities as 2D coordinates and visualizes the optimal path found during generations.

## Project Structure

```
├── src/
│   └── src.py
├── visualizations/
│   |── best_found_route.png
│   └── convergence_curve.png
├── .gitignore
└── README.md
```
