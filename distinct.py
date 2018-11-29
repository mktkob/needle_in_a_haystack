import numpy as np


def binarize(dst):
    # print(np.max(dst) - np.min(dst))
    # if np.max(dst) > 150:
    # if np.std(dst) > 20:
    if np.max(dst) - np.min(dst) > 80:
        return '1'
    else:
        return '0'


def binarize_dawn(dst):
    # print(np.max(dst) - np.min(dst))
    if np.max(dst) - np.min(dst) > 30:
        return '1'
    else:
        return '0'


def binarize_daylight(dst):
    # print(np.max(dst) - np.min(dst))
    if np.max(dst) - np.min(dst) > 90:
        return '1'
    else:
        return '0'
