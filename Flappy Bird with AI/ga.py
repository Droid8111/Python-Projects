import random
import numpy as np  # Import numpy for array operations
from neural_network import NeuralNetwork

class BirdAI:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 1
        self.lift = -13
        self.radius = 15
        self.brain = NeuralNetwork(7, 10, 1)  # Updated input size to 7
        self.fitness = 0

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = self.lift

    def think(self, next_pillar, next_next_pillar):
        top, bottom, _ = next_pillar
        gap_center = top.height + (bottom.y - top.height) / 2

        # Use second pillar if available
        if next_next_pillar:
            top2, bottom2, _ = next_next_pillar
            gap_center2 = top2.height + (bottom2.y - top2.height) / 2
            x2_relative = (top2.x - self.x) / 800
            gap2_relative = (gap_center2 - self.y) / 600
        else:
            x2_relative = 1.0
            gap2_relative = 0.0

        inputs = np.array([
            self.y / 600,
            np.tanh(self.velocity / 20),
            (top.x - self.x) / 800,
            (gap_center - self.y) / 600,
            (self.velocity - (gap_center - self.y)) / 200,
            x2_relative,
            gap2_relative
        ])
        output = self.brain.forward(inputs)
        if output[0] > 0.5:
            self.jump()


def select_parent(pop):
    r = random.random()
    cumulative = 0
    for b in pop:
        cumulative += b.fitness
        if cumulative >= r:
            return b
    return pop[-1]


def next_generation(old_birds, mutation_rate, start_x=100, start_y=300, global_champion=None):
    total = sum(b.fitness for b in old_birds)
    if total == 0:
        return [BirdAI(start_x, start_y) for _ in old_birds], global_champion

    old_birds.sort(key=lambda b: b.fitness, reverse=True)

    if global_champion is None or old_birds[0].fitness > global_champion.fitness:
        global_champion = old_birds[0]

    new_pop = []
    elite_count = 15
    for i in range(elite_count):
        elite = BirdAI(start_x, start_y)
        elite.brain = old_birds[i].brain.copy()
        new_pop.append(elite)

    champ = BirdAI(start_x, start_y)
    champ.brain = global_champion.brain.copy()#
    new_pop.append(champ)

    for _ in range(len(old_birds) - elite_count - 1):
        parent = select_parent(old_birds)
        child = BirdAI(start_x, start_y)
        child.brain = parent.brain.copy()
        child.brain.mutate(mutation_rate)
        new_pop.append(child)

    return new_pop, global_champion