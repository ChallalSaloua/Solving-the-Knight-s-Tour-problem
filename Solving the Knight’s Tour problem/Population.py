#population.py
import random
from Chromosome import Chromosome
from Knight import Knight

class Population:
    """
    Gère population/dynamiques, conforme TD Profs.
    """
    def __init__(self, population_size):
        self.population_size = population_size
        self.generation = 1
        self.knights = [Knight() for _ in range(population_size)]

    def check_population(self):
        for knight in self.knights:
            knight.check_moves()

    def evaluate(self):
        max_fit = -1
        best_solution = None
        for knight in self.knights:
            knight.evaluate_fitness()
            if knight.fitness > max_fit:
                max_fit = knight.fitness
                best_solution = knight
        return max_fit, best_solution

    def tournament_selection(self, size=3):
        candidates = random.sample(self.knights, size)
        candidates.sort(key=lambda k: k.fitness, reverse=True)
        return candidates[0], candidates[1]

    def create_new_generation(self, mutation_rate=0.001):
        new_knights = []
        while len(new_knights) < self.population_size:
            parent1, parent2 = self.tournament_selection()
            child1_chromo, child2_chromo = parent1.chromosome.crossover(parent2.chromosome)
            child1_chromo.mutation(mutation_rate)
            child2_chromo.mutation(mutation_rate)
            new_knights.append(Knight(child1_chromo))
            if len(new_knights) < self.population_size:
                new_knights.append(Knight(child2_chromo))
        self.knights = new_knights
        self.generation += 1
