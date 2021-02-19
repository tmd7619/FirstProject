from django.conf import settings
import numpy as np
import cv2
import pyautogui
from threading import Timer
flag = 1

def timefunction():
    print('timefunction')
    global flag
    flag = 0
    return 0

def opencv_browser(start):
    flag = start
    timeout = 10
    t = Timer(timeout, timefunction)
    t.start()

    target = cv2.imread('./media/qr2_img.png', cv2.IMREAD_GRAYSCALE)
    h, w = target.shape

    if(type(target) is np.ndarray):

        while flag:
            _img = np.array(pyautogui.screenshot())
            img = cv2.cvtColor(_img, cv2.COLOR_RGB2GRAY)
            result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
            minValue, maxValue, minLoc, maxLoc = cv2.minMaxLoc(result)
            leftTop = maxLoc

            # maxValue == 0.8
            filtered = _img
            rightBottom = maxLoc[0] + h, maxLoc[1] + w

            if maxValue >= 0.8:
                print(maxValue)
                cv2.rectangle(_img, leftTop, rightBottom, (255, 255, 0), 3)
                cropping = _img[leftTop[1]:rightBottom[1], leftTop[0]:rightBottom[0]]
                filtered = 0
                filtered = cropping
                cv2.imwrite('./media/qr_img.png', filtered)
                t.cancel()
                return 1

    else:
        print('something error or time out')
        t.cancel()
    return 0