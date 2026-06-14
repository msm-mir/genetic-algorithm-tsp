import random
import math

# generate coordinate (x, y) of n cities
def generate_cities(n):
    cities_set = set()

    while len(cities_set) < n:
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)

        cities_set.add((x, y))
    
    return list(cities_set)

# calculate distance matrix for all pairs of cities
def distance_of_cities(cities):
    # euclidean distance
    def dis(c1, c2):
        x1, y1 = c1
        x2, y2 = c2
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    # n*n distance matrix
    distance_matrix = [[dis(c1, c2) for c2 in cities] for c1 in cities]
    return distance_matrix


# generate inputs (coordinate of the cities)
n_cities = 100
cities = generate_cities(n_cities)

# euclidean distance for city pairs
distance_matrix = distance_of_cities(cities)

# generate initial population
init_pop = [random.sample(range(n_cities), n_cities) for _ in range(n_cities)]