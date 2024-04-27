import numpy as np
from scipy.optimize import curve_fit
from osd.unit import OShapedUnit, VShapedUnit, HTNUnit
from osd.stimulus import Stimulus


def feng_htn(x, e11, i11,
             e21, i21,
             e31, w1, w2, w3, w4, w5, gain):

    return htn(x, e11, 0.2, 0, 0.01, i11, 0.2, 0, 0.01,
             e21, 0.2, 0, 0.01, i21, 0.2, 0, 0.01,
             e31, 0.2, 0, 0.01, w1, w2, w3, w4, w5, gain)


# [cf, bw, bias, wa][0:5], input_weights[0:5], gain
def htn(x, *args):

    if x.ndim == 3:
        return [htn(sub, *args) for sub in x]
    else:
        pass

    param_e1 = args[0:4]
    param_i1 = args[4:8]
    param_e2 = args[8:12]
    param_i2 = args[12:16]
    param_e3 = args[16:20]
    input_weights = args[20:25]
    gain = args[25]

    e1 = VShapedUnit(*param_e1)
    i1 = VShapedUnit(*param_i1)
    e2 = VShapedUnit(*param_e2)
    i2 = VShapedUnit(*param_i2)
    e3 = VShapedUnit(*param_e3)

    htn_unit = HTNUnit([e1, i1, e2, i2, e3], input_weights, gain)
    data = np.reshape(x, (3, -1))
    stimulus = Stimulus(data=data)

    return htn_unit.rate(stimulus)


class Fitter:
    def __init__(self):
        pass

    def fit(self, stimuli, results):
        x_data = [stimulus._data.reshape(1, -1) for stimulus in stimuli]
        y_data = [result[0] for result in results]

        lower_bound = [0.1,
                       0.1,
                       0.1,
                       0.1,
                       0.1,
                       0, -1, 0, -1, 0, 0.1]

        upper_bound = [32,
                       32,
                       32,
                       32,
                       32,
                       1, 0, 1, 0, 1, 10]

        popt, pcov = curve_fit(feng_htn, x_data, y_data, bounds=(lower_bound, upper_bound))

        return popt
