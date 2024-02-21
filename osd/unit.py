from abc import ABC, abstractmethod
import numpy as np


# defines a single unit with rate-stimulus function
class Unit(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__()

    @abstractmethod
    def rate(self, stimulus) -> float:
        return -1.0


# assume Gaussian frequency-rate tuning curve and linear level-rate tuning curve
class VShapedUnit(Unit):
    def __init__(self, characteristic_frequency=1000, bandwidth=200, weight_amplitude=0.1, bias=0.5, **kwargs):
        super().__init__(**kwargs)
        self.cf = characteristic_frequency
        self.bw = bandwidth
        self.bias = bias            # positive bias ~ threshold, negative bias ~ spontaneous rate
        self.wa = weight_amplitude  # level-rate coefficient at CF

    def rate(self, stimulus):
        weights = self.wa * np.exp(-((stimulus.frequencies - self.cf) / self.bw) ** 2 / 2)
        input = np.dot(weights, stimulus.levels) - self.bias

        return 1 / (1 + np.exp(-input))




