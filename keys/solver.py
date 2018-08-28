"""
You'll need opencv, numpy, pymouse, mss
Simply run solver.py and watch it do its magic.
"""

import time
import autopy
import imutils

import cv2
import mss
import numpy
from scipy.misc import imsave
from pymouse import PyMouse

m = PyMouse()

def click(x,y):
    # win32api.SetCursorPos((x,y))
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    m.click(x, y, 1)

def f(img):
    greenLower = (101, 0, 0)
    greenUpper = (108, 255, 255)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    grnn = cv2.inRange(hsv, (73, 197, 173), (74, 198, 174))

    cnts = cv2.findContours(grnn.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        grnn[y:y+h, x:x+w] = 255
    else:
        return None


    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = mask * grnn

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            return center

with mss.mss() as sct:
    monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

    while True:
        img = numpy.array(sct.grab(monitor))
        center = f(img)
        if not center is None:
            click(center[0], center[1])
        