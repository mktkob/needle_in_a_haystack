import numpy as np
import glob
import cv2


def binarize(dst):
    if np.max(dst) - np.min(dst) > 80:
        return '1'
    else:
        return '0'


def binarize_dawn(dst):
    if np.max(dst) - np.min(dst) > 30:
        return '1'
    else:
        return '0'


def binarize_daylight(dst):
    if np.max(dst) - np.min(dst) > 90:
        return '1'
    else:
        return '0'


def import_figures(directory_name):
    file_list = sorted(glob.glob(directory_name + '/*.png'))
    morse_sequence = ''
    for file_name in file_list:
        im = cv2.imread(file_name, 0)
        dst = im[585:595, 1135:1150]
        if int(file_name[20:23]) < 400:
            degitized_sequence = binarize(dst)
        elif int(file_name[20:23]) < 427:
            degitized_sequence = binarize_dawn(dst)
        else:
            degitized_sequence = binarize_daylight(dst)
        morse_sequence = morse_sequence + degitized_sequence
        # print(file_name[20:])
        cv2.imwrite('converted/' + file_name[7:], dst)
        # For confirming the window recognition
    return morse_sequence
