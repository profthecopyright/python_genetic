import json

import numpy as np
from osd.stimulus import Stimulus
from osd.unit import VShapedUnit, OShapedUnit
from osd.ga_stimulus_generator import GAStimulusGeneratorConfig, GAStimulusGenerator


class Experiment:
    def __init__(self):
        # self.unit = VShapedUnit()
        self.unit = OShapedUnit()

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

    total_batches = 50

    print("Experiment Starts.\n")

    for k in range(total_batches):
        print(f"Generating Batch {k}...")
        stimuli = stim_gen.generate_stimuli()
        print(f"Stimuli Batch {k} Generated (size = {len(stimuli)}). Testing...")
        results = experiment.test(stimuli)
        print(f"Batch {k} tested. Max Readout = {max(results)}")
        print("Updating Stimulus Generator...")
        stim_gen.update_results(results)
        print(f"Batch {k} Finished.\n")

    print("\nExperiment Done.")

    print(stim_gen.all_records[-1][:10])


if __name__ == '__main__':
    main_test()
