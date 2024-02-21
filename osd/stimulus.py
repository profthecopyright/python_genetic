import numpy as np


class Stimulus:
    def __init__(self, frequencies=None, levels=None, phases=None, data=None):
        if data is not None:
            self._data = np.asarray(data, dtype=np.float64)

            if self._data.ndim == 2 and self._data.shape[0] >= 3:
                self._data = self._data[:3, :]
            else:
                raise Exception('Use a k-by-3 array-like object to initialize a Stimulus via "data" argument')
        else:
            self._data = np.ndarray(shape=(3, len(frequencies)), dtype=np.float64)

            if frequencies is not None:
                self._data[0, :] = frequencies
            else:
                pass

            if levels is not None:
                self._data[1, :] = levels
            else:
                pass

            if phases is not None:
                self._data[2, :] = phases
            else:
                pass

    @property
    def frequencies(self):
        return self._data[0, :]

    @property
    def levels(self):
        return self._data[1, :]

    @property
    def phases(self):
        return self._data[2, :]

    @frequencies.setter
    def frequencies(self, value):
        self._data[0, :] = value

    @levels.setter
    def levels(self, value):
        self._data[1, :] = value

    @phases.setter
    def phases(self, value):
        self._data[2, :] = value

    def __repr__(self):
        return f"Stimulus <components={self._data.shape[1]}, f={self.frequencies}, A={self.levels}, p={self.phases}>"
