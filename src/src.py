import random
import math
import time
import matplotlib.pyplot as plt

class GA:
    def __init__(self, cities, pop_size, n_generations, mutation_rate):
        self.cities = cities
        self.n_cities = len(self.cities)
        self.pop_size = pop_size
        self.n_generations = n_generations
        self.mutation_rate = mutation_rate

        self.best_distance = float('inf')
        self.best_distance_history = []
        self.best_tour = None
        
        random.seed(42)

        # euclidean distance for city pairs
        self.dis_mx = self.distance_of_cities()

        # generate initial population
        self.population = self.generate_init_pop()

    # calculate distance matrix for all pairs of cities
    def distance_of_cities(self):
        # euclidean distance
        def dis(c1, c2):
            x1, y1 = c1
            x2, y2 = c2
            return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

        # n*n distance matrix
        distance_matrix = [[dis(c1, c2) for c2 in self.cities] for c1 in self.cities]
        return distance_matrix
    
    # generate the initial population of chromosomes
    def generate_init_pop(self):
        return [
            # each chromosome is a random permutation of all city indices
            random.sample(range(self.n_cities), self.n_cities)
            for _ in range(self.pop_size)
        ]
    
    # compute the fitness score of a chromosome
    def cal_fitness(self, chromosome):
        total_distance = 0
        n = len(chromosome)

        # sum the distances between cities sequentially in the chromosome
        for i in range(n):
            first_city = chromosome[i]
            sec_city = chromosome[(i + 1) % n] # for distance between the last city and the first city
            
            total_distance += self.dis_mx[first_city][sec_city]
        
        # aim of the algorithm is to maximize fitness
        return 1.0 / total_distance

    # tournament selection to generate a parent
    def tournament_selection(self, fitness_scores, best_score_idx, tourn_size=3):
        # remove the best score index from the selection pool
        available_idx = list(set(range(len(self.population))) - {best_score_idx})
        # randomly select chromosomes for the tournament
        selected_tourn = random.sample(available_idx, tourn_size)

        # find the index of the tournament participant with the highest fitness score
        selected_idx = max(selected_tourn, key=lambda t: fitness_scores[t])

        # return the best parent chosen by tournament
        return self.population[selected_idx]

    # order crossover to generate the child
    def order_crossover(self, parent1, parent2):
        n = len(parent1)

        # generate two random cut points for the parents
        cut1 = random.randint(0, n - 2)
        cut2 = random.randint(cut1 + 1, n - 1)

        # fill the child with -1 initial values of parent size
        child = [-1 for _ in range(n)]

        # copy the middle section of the parent to the child
        child[cut1:cut2] = parent2[cut1:cut2]

        # collect the remaining genes from parent starting at cut2 and wrapping around
        remaining_genes = parent1[cut2:] + parent1[:cut2]

        # remove genes already present in child's middle section
        child_set = set(child[cut1:cut2])
        remaining_genes = [g for g in remaining_genes if g not in child_set]

        # target indices in the child to fill: start at cut2, continue to end, then wrap to start
        target_indices = list(range(cut2, n)) + list(range(0, cut2))

        # fill the remaining indices in the child with the remaining genes
        for i in range(len(remaining_genes)):
            idx = target_indices[i]
            child[idx] = remaining_genes[i]
        
        return child

    # inversion mutation for a chromosome
    def inversion_mutation(self, chromosome):
        n = len(chromosome)

        # generate two random cut points for the inversion mutation
        cut1 = random.randint(0, n - 2)
        cut2 = random.randint(cut1 + 1, n - 1)

        c = list(chromosome)

        # copy the chromosome with its middle section inverted
        mutated_chr = c[:cut1] + c[cut1:cut2][::-1] + c[cut2:]
        
        return mutated_chr

    # performs selection, crossover, and mutation over multiple generations
    def fit(self):
        for g in range(self.n_generations):
            # store fitness score of each chromosome in the population
            fitness_scores = [self.cal_fitness(self.dis_mx, p) for p in self.population]
            # store best score to pass it directly to the next generation
            max_score = max(fitness_scores)
            best_score_idx = fitness_scores.index(max_score)
            best_chromosome = self.population[best_score_idx]

            # for convergence plot
            current_best_dis = 1.0 / max_score
            self.best_distance_history.append()

            if current_best_dis < self.best_distance:
                self.best_distance = current_best_dis
                self.best_tour = best_chromosome

            # create new population for the next generation
            new_pop = [best_chromosome]

            while len(new_pop) < self.pop_size:
                # generate parents using tournament selection
                parent1 = self.tournament_selection(fitness_scores, best_score_idx) 
                parent2 = self.tournament_selection(fitness_scores, best_score_idx) 

                # produce children using order crossover
                child1 = self.order_crossover(parent1, parent2)
                child2 = self.order_crossover(parent2, parent1)

                # apply inversion mutation to children based on the mutation rate
                if random.random() < self.mutation_rate:
                    child1 = self.inversion_mutation(child1)
                if random.random() < self.mutation_rate:
                    child2 = self.inversion_mutation(child2)

                # add children to the new population
                new_pop.append(child1)
                new_pop.append(child2)
            
            self.population = new_pop


# generate coordinate (x, y) of n cities
def generate_cities(n_cities):
    # use a set to avoid duplicate coordinates
    cities_set = set()

    while len(cities_set) < n_cities:
        # use uniform to generate float coordinate
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)

        cities_set.add((x, y))
    
    return list(cities_set)

# visualize the convergence by plotting the best distance across generations
def convergence_plot(history):
    plt.figure(figsize=(8, 4))
    plt.plot(history, color="violet", linewidth=2, label="Best Distance")

    plt.title("Genetic Algorithm Convergence for TSP", fontsize=14, fontweight="bold")
    plt.xlabel("Generation", fontsize=12)
    plt.ylabel("Total Distance", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()

    plt.show()

# plotting the best route
def plot_best_route(cities, best_tour):
    closed_tour = best_tour + [best_tour[0]]

    x = [cities[tour_idx][0] for tour_idx in closed_tour]
    y = [cities[tour_idx][1] for tour_idx in closed_tour]

    plt.figure(figsize=(8, 4))

    plt.plot(x, y, color="violet", linestyle="-", linewidth=2, marker="o")

    plt.scatter(
        [c[0] for c in cities],
        [c[1] for c in cities],
        color="black",
        s=30,
        zorder=5,
    )

    plt.scatter(
        cities[best_tour[0]][0],
        cities[best_tour[0]][1],
        color="green",
        s=50,
        label="Start City",
        zorder=6,
    )

    plt.title("Best Found TSP Route", fontsize=14, fontweight="bold")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.show()


# generate coordinate of the cities
cities = generate_cities(n_cities=50)

my_model = GA(cities, pop_size=500, n_generations=800, mutation_rate=0.05)

start_time = time.time()
my_model.fit()
exec_time = time.time() - start_time

print(f'\n execution time: {exec_time:.3f}\n\n')

convergence_plot(my_model.best_distance_history)
plot_best_route(cities, my_model.best_tour)