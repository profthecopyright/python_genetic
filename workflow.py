import json

import numpy as np
import matplotlib.pyplot as plt
from osd.stimulus import Stimulus
from osd.unit import VShapedUnit, OShapedUnit, HTNUnit
from osd.ga_stimulus_generator import GAStimulusGeneratorConfig, GAStimulusGenerator


class Experiment:
    def __init__(self):
        self.e1 = VShapedUnit(characteristic_frequency=3, weight_amplitude=0.01)
        self.e2 = VShapedUnit(characteristic_frequency=6, weight_amplitude=0.01)
        self.e3 = VShapedUnit(characteristic_frequency=9, weight_amplitude=0.01)
        self.i1 = VShapedUnit(characteristic_frequency=4.5, weight_amplitude=0.01, bandwidth=1)
        self.i2 = VShapedUnit(characteristic_frequency=7.5, weight_amplitude=0.01, bandwidth=1)
        self.unit = HTNUnit([self.e1, self.i1, self.e2, self.i2, self.e3], [0.3, -0.2, 0.5, -0.2, 0.3], 1)

    # a simple simulation of an experiment.
    # The return value should be a list of 1D array (currently only the mean is considered for now!).
    def test(self, stimuli: list[Stimulus]):
        return np.asarray([[self.unit.rate(stimulus)] for stimulus in stimuli])


def main_test():
    experiment = Experiment()

    with open("gasg_config.json", "r") as f:
        d = json.load(f)

    config = GAStimulusGeneratorConfig(**d)
    stim_gen = GAStimulusGenerator(config=config)

    total_batches = 20

    print("Experiment Starts.\n")

    readouts = []

    for k in range(total_batches):
        print(f"Generating Batch {k}...")
        stimuli = stim_gen.generate_stimuli()
        print(f"Stimuli Batch {k} Generated (size = {len(stimuli)}). Testing...")
        results = experiment.test(stimuli)
        print(f"Batch {k} tested. Max Readout = {max(results)}")
        readouts.append(max(results)[0])
        print("Updating Stimulus Generator...")
        stim_gen.update_results(results)
        print(f"Batch {k} Finished.\n")

    print("\nExperiment Done.")

    print(stim_gen.all_records[-1][:10])
    print(readouts)

    plt.plot(readouts)
    plt.xlabel('Generation')
    plt.ylabel('readout')
    plt.show()


if __name__ == '__main__':
    main_test()
