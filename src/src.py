import random

# generate coordinate (x, y) of n cities
def generate_cities(n):
    cities_set = set()

    while len(cities_set) < n:
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)

        cities_set.add((x, y))
    
    return list(cities_set)

# generate inputs (coordinate of the cities)
n_cities = 100
cities = generate_cities(n_cities)