import cv2;
import numpy as np
from collections import defaultdict

THRESHOLD = 0.7

def removeDetected(img, row, col, box_width, box_height):
    top = -1
    bottom = -1
    for height in range(0, box_height):
        cur_width = 0
        for width in range(0, box_width):
            if img[row + height][col + width] != 255:
                cur_width += 1
        if cur_width > 1:
            if bottom == -1:
                bottom = row + height
            else:
                top = row + height
            for width in range(0, box_width):
                img[row + height][col + width] = 255
    return bottom, top

def detectSymbols(original, marked, template):
    symbols = defaultdict(lambda: defaultdict(dict))
    #print index
    w, h = template.shape[::-1]
    #print img.shape

    res = cv2.matchTemplate(original, template, cv2.TM_CCOEFF_NORMED)

    template = template.copy()
    #cv2.line(note, (0, h/2), (w, h/2), (0 , 0, 0))
    loc = np.where(res >= THRESHOLD)

    for pt in zip(*loc[::-1]):
        symbols[pt[0]][pt[1]]["bottom"] = -1
        symbols[pt[0]][pt[1]]["top"] = -1

    return symbols
