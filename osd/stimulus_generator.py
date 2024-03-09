from abc import ABC, abstractmethod

from osd.stimulus import Stimulus


class StimulusGenerator(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__()

    @abstractmethod
    def generate_stimuli(self, **kwargs) -> list:
        return []

    @abstractmethod
    def update_results(self, results, **kwargs):
        pass
