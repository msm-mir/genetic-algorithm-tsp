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

# compute the fitness function of a chromosome
def fitness_function(dis_mx, chromosome):
    total_distance = 0
    n = len(chromosome)

    # sum the distances between cities sequentially in the chromosome
    for i in range(n):
        first_city = chromosome[i]
        sec_city = chromosome[(i + 1) % n] # for distance between the last city and the first city
        
        total_distance += dis_mx[first_city][sec_city]
    
    # aim of the algorithm is to maximize fitness
    return 1 / total_distance

# tournament selection to generate a parent
def tournament_selection(pop, dis_mx, tourn_size=3):
    # store fitness score of each chromosome in the population
    fitness_scores = [fitness_function(dis_mx, p) for p in pop]
    # store best score to pass it directly to the next generation
    max_score = max(fitness_scores)
    best_score_idx = fitness_scores.index(max_score)
    
    # remove the best score index from the selection pool
    available_idx = list(set(range(len(pop))) - {best_score_idx})
    # randomly select chromosomes for the tournament
    selected_tourn = random.sample(available_idx, tourn_size)

    # find the index of the tournament participant with the highest fitness score
    selected_idx = max(selected_tourn, key=lambda t: fitness_scores[t])

    # return the best parent chosen by tournament
    return pop[selected_idx]


random.seed(42)

# generate inputs (coordinate of the cities)
n_cities = 100
cities = generate_cities(n_cities)

# euclidean distance for city pairs
dis_mx = distance_of_cities(cities)

# generate initial population
pop_size = 100
init_pop = [random.sample(range(n_cities), n_cities) for _ in range(pop_size)]

