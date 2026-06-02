#chromosome.py
import random

class Chromosome:
    """
    Chromosome conforme au TD Knight's Tour : 63 gènes ∈ [1,8], croisement simple-point, mutation faible.
    """
    def __init__(self, genes=None):
        if genes is None:
            self.genes = [random.randint(1, 8) for _ in range(63)]
        elif len(genes) == 63:
            self.genes = genes.copy()
        else:
            raise ValueError("Un chromosome doit avoir exactement 63 gènes.")

    def crossover(self, partner):
        """Croisement mono-point (TD)."""
        point = random.randint(1, len(self.genes) - 1)
        child1 = self.genes[:point] + partner.genes[point:]
        child2 = partner.genes[:point] + self.genes[point:]
        return Chromosome(child1), Chromosome(child2)

    def mutation(self, mutation_rate=0.001):
        """Mutation faible proba (TD/Projet)."""
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = random.randint(1, 8)

