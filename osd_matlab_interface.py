import numpy as np

from osd.ga_stimulus_generator import GAStimulusGeneratorConfig, GAStimulusGenerator
from osd.unit import VShapedUnit, OShapedUnit
from stream.stream_agent import StreamAgent


# Matlab 2017a compatibility interface
def to_ndarray(vec, n_row, n_col):
    arr = np.asarray(vec)
    return arr.reshape((int(n_row), int(n_col)), order='F')
