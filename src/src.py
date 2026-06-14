import random
import math

# generate coordinate (x, y) of n cities
def generate_cities(n):
    # use a set to avoid duplicate coordinates
    cities_set = set()

    while len(cities_set) < n:
        # use uniform to generate float coordinate
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

# order crossover to generate children
def crossover_ox(parent1, parent2):
    n = len(parent1)

    # generate two random cut points for the parents
    cut1 = random.randint(0, n - 2)
    cut2 = random.randint(cut1 + 1, n - 1)

    # fill the children with -1 initial values of parent size
    child1 = [-1 for _ in range(n)]
    child2 = [-1 for _ in range(n)]

    # copy the middle section of the parents to the children
    child1[cut1:cut2] = parent2[cut1:cut2]
    child2[cut1:cut2] = parent1[cut1:cut2]

    # collect the remaining genes from each parent starting at cut2 and wrapping around
    remaining_genes1 = parent1[cut2:] + parent1[:cut2]
    remaining_genes2 = parent2[cut2:] + parent2[:cut2]

    # remove genes already present in each child's middle section
    remaining_genes1 = [g for g in remaining_genes1 if g not in child1]
    remaining_genes2 = [g for g in remaining_genes2 if g not in child2]

    # target indices in the child to fill: start at cut2, continue to end, then wrap to start
    target_indices = list(range(cut2, n)) + list(range(0, cut2))

    # fill the remaining indices in each child with the remaining genes
    for i in range(len(remaining_genes1)):
        idx = target_indices[i]
        child1[idx] = remaining_genes1[i]
        child2[idx] = remaining_genes2[i]
    
    return child1, child2


random.seed(42)

# generate inputs (coordinate of the cities)
n_cities = 100
cities = generate_cities(n_cities)

# euclidean distance for city pairs
dis_mx = distance_of_cities(cities)

# generate initial population
pop_size = 100
init_pop = [random.sample(range(n_cities), n_cities) for _ in range(pop_size)]

