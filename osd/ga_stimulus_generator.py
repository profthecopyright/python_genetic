from dataclasses import dataclass
from typing import Any

from osd.stimulus_generator import StimulusGenerator
from osd.stimulus import Stimulus

import numpy as np


@dataclass
class GAStimulusGeneratorConfig:
    min_freq: float
    max_freq: float
    min_level: float
    max_level: float
    component_num: int
    population_size: int
    elite_num: int
    max_iter: int
    frequency_sigma: float
    level_sigma: float
    mutation_rate: float
    cross_top: float



@dataclass
class DataRecord:
    stimulus: Stimulus
    result: Any


class GAStimulusGenerator(StimulusGenerator):
    def __init__(self, config: GAStimulusGeneratorConfig):
        super().__init__()
        self.config = config
        self._reset()

    def generate_stimuli(self, **kwargs) -> list:
        if not self.all_records:
            return self._generate_first_batch()
        elif self.current_iter >= self.config.max_iter:
            raise Exception('generate_stimuli(): current_iter > max_iter!')
        else:
            return self._generate_next_batch()

    def update_results(self, results, **kwargs):
        if self.current_iter < self.config.max_iter:
            for k in range(len(results)):
                result = results[k]
                self.all_records[self.current_iter][k].result = result
        else:
            raise Exception('update_results(): current_iter > max_iter!')

    # ================== Helper Methods Below ============================

    def _reset(self):
        self.current_iter = 0
        self.all_records = []

    def _generate_first_batch(self):
        shape = (self.config.population_size, self.config.component_num)
        freqs = np.random.uniform(self.config.min_freq, self.config.max_freq, shape)
        levels = np.random.uniform(self.config.min_level, self.config.max_level, shape)
        phases = np.random.uniform(0, 2 * np.pi, shape)

        stimuli = [Stimulus(frequencies=freqs[k, :], levels=levels[k, :], phases=phases[k, :])
                   for k in range(self.config.population_size)]

        records = [DataRecord(stimulus=stimuli[k], result=None) for k in range(self.config.population_size)]
        self.all_records.append(records)
        self.current_iter = 0

        return list(stimuli)    # copy to avoid occasional modifications

    def _fitness(self, record: DataRecord):
        if record.result is None:
            return 0
        elif isinstance(record.result, (int, float)):
            return record.result
        else:
            return np.mean(record.result)

    def _cross(self, parent_stimulus1, parent_stimulus2):
        half1 = int(self.config.component_num / 2)
        half2 = self.config.component_num - half1

        indices1 = np.random.choice(self.config.component_num, half1)
        indices2 = np.random.choice(self.config.component_num, half2)

        child_frequencies = np.append(parent_stimulus1.frequencies[indices1], parent_stimulus2.frequencies[indices2])
        multiplier = np.random.choice([0, 1], self.config.component_num,
                                      p=[1 - self.config.mutation_rate, self.config.mutation_rate])
        child_frequencies += multiplier * np.random.normal(0, self.config.frequency_sigma, self.config.component_num)
        child_frequencies[child_frequencies < self.config.min_freq] = self.config.min_freq
        child_frequencies[child_frequencies > self.config.max_freq] = self.config.max_freq

        child_levels = np.append(parent_stimulus1.levels[indices1], parent_stimulus2.levels[indices2])
        multiplier = np.random.choice([0, 1], self.config.component_num,
                                      p=[1 - self.config.mutation_rate, self.config.mutation_rate])
        child_levels += multiplier * np.random.normal(0, self.config.level_sigma, self.config.component_num)
        child_levels[child_levels < self.config.min_level] = self.config.min_level
        child_levels[child_levels > self.config.max_level] = self.config.max_level

        child_phases = np.append(parent_stimulus1.phases[indices1], parent_stimulus2.phases[indices2])
        # todo: phase cross

        return Stimulus(frequencies=child_frequencies, levels=child_levels, phases=child_phases)

    def _generate_next_batch(self):
        last_records = sorted(self.all_records[self.current_iter], key=self._fitness, reverse=True)
        last_stimuli = [record.stimulus for record in last_records]

        elite_stimuli = last_stimuli[:self.config.elite_num]

        # todo: add theoretical prediction(s)
        child_num = self.config.population_size - self.config.elite_num

        cross_num = int(self.config.population_size * self.config.cross_top)    # num of parent candidates

        fitnesses = np.asarray([self._fitness(record) for record in last_records[:cross_num]])
        choice_probs = fitnesses / np.sum(fitnesses)    # normalize

        mothers = np.random.choice(last_stimuli[:cross_num], child_num, p=choice_probs)
        fathers = np.random.choice(last_stimuli[:cross_num], child_num, p=choice_probs)
        child_stimuli = [self._cross(mothers[i], fathers[i]) for i in range(child_num)]

        new_stimuli = elite_stimuli + child_stimuli

        new_records = [DataRecord(stimulus=stimulus, result=None) for stimulus in new_stimuli]

        self.all_records.append(new_records)
        self.current_iter += 1

        return list(new_stimuli)
