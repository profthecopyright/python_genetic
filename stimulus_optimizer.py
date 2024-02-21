from osd.stimulus import Stimulus
from osd.unit import VShapedUnit


class StimulusOptimizer:
    def __init__(self):
        self.iter = 0
        self.min_freq = 0.5
        self.max_freq = 16

        self.min_level = 0
        self.max_level = 60

        self.n_component = 20
        self.n_population = 100

        self.n_elite = 10
        self.n_iter = 100

        self.freq_sigma = 0.05
        self.level_sigma = 10

        self.mutation_rate = 0.1

    def solve(self):
        pass


if __name__ == '__main__':
    unit = VShapedUnit()
    stimulus = Stimulus(frequencies=[500, 2000, 3000, 4000], levels=[20, 60, 20, 20])

    print(unit.rate(stimulus))
