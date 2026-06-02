#knight.py
import random
from Chromosome import Chromosome

class Knight:
    """
    Cavalier : simulation génétique du tour – fidèle au TD.
    """
    MOVES = {
        1: (1, 2), 2: (2, 1), 3: (2, -1), 4: (1, -2),
        5: (-1, -2), 6: (-2, -1), 7: (-2, 1), 8: (-1, 2)
    }
    def __init__(self, chromosome=None):
        self.chromosome = Chromosome() if chromosome is None else chromosome
        self.position = (0, 0)
        self.path = [(0, 0)]
        self.fitness = 0
        self.is_valid = True

    def move_forward(self, direction):
        dx, dy = self.MOVES[direction]
        return self.position[0] + dx, self.position[1] + dy

    def move_backward(self):
        if len(self.path) > 1:
            self.path.pop()
            self.position = self.path[-1]
    
    def _try_move(self, direction, occupied):
        nx, ny = self.move_forward(direction)
        if 0 <= nx < 8 and 0 <= ny < 8 and (nx, ny) not in occupied:
            self.position = (nx, ny)
            self.path.append(self.position)
            return True
        return False

    def check_moves(self):
        self.position = (0, 0)
        self.path = [(0, 0)]
        self.is_valid = True
        occupied = set(self.path)
        cycle_direction = 'forward' if random.random() < 0.5 else 'backward'
        for gene in self.chromosome.genes:
            moved = False
            for i in range(8):
                move_to_try = (
                    (gene - 1 + i) % 8 + 1 if cycle_direction == 'forward'
                    else (gene - 1 - i) % 8 + 1
                )
                if self._try_move(move_to_try, occupied):
                    occupied.add(self.position)
                    moved = True
                    break
            if not moved:
                self.is_valid = False
                break  # TD : stop path if no move possible
    def evaluate_fitness(self):
        self.fitness = len(set(self.path))
