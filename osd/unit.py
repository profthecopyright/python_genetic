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
    def __init__(self, characteristic_frequency=4, bandwidth=0.2, weight_amplitude=0.001, bias=0, **kwargs):
        super().__init__(**kwargs)
        self.cf = characteristic_frequency  # kHz
        self.bw = bandwidth         # kHz
        self.bias = bias            # positive bias ~ threshold, negative bias ~ spontaneous rate
        self.wa = weight_amplitude  # level-rate coefficient at CF

    def rate(self, stimulus):
        weights = self.wa * np.exp(-((stimulus.frequencies - self.cf) / self.bw) ** 2 / 2)
        input = np.dot(weights, stimulus.levels) - self.bias

        return 1 / (1 + np.exp(-input))


# assume Gaussian frequency-rate tuning curve and Gaussian level-rate tuning curve
class OShapedUnit(Unit):
    def __init__(self, characteristic_frequency=4, bandwidth=0.2, weight_amplitude=0.1, best_level=30, sigma_level=10, bias=0, **kwargs):
        super().__init__(**kwargs)
        self.cf = characteristic_frequency  # kHz
        self.bw = bandwidth         # kHz
        self.bias = bias            # positive bias ~ threshold, negative bias ~ spontaneous rate
        self.wa = weight_amplitude  # level-rate coefficient at CF
        self.bl = best_level
        self.sl = sigma_level

    def rate(self, stimulus):
        weights = self.wa * np.exp(-((stimulus.frequencies - self.cf) / self.bw) ** 2 / 2)
        level_multipliers = np.exp(-((stimulus.levels - self.bl) / self.sl) ** 2 / 2)
        input = np.dot(weights, level_multipliers) - self.bias

        return 1 / (1 + np.exp(-input))
