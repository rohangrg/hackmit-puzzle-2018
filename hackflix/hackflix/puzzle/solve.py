from config import *

import imageio
import numpy as np
import cv2
from skimage.restoration import inpaint

import matplotlib.pyplot as plt

def solve_frame(image):
    h, w, c = image.shape
    wt_size = 128

    mask = np.zeros((h, w), dtype=np.uint8)
    mask[h-10-wt_size:h-10, 10:10+wt_size] = 1

    # res = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
    res = inpaint.inpaint_biharmonic(image, mask, multichannel=True)

    return res

def process_video(vid):
    vid = imageio.get_reader(vid, 'ffmpeg')
    writer = imageio.get_writer("solved.mp4", 'ffmpeg', fps=vid.get_meta_data()['fps'], quality=10)
    c = 0
    for image in vid:
        c+=1
        print c
        writer.append_data(solve_frame(image))
    writer.close()

if __name__ == '__main__':
    process_video("op.mp4")
