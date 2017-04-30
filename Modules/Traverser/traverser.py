import cv2
import numpy as np

def __check_bound(img, x, y):
    w, h = img.shape[::-1]
    return x >= 0 and y >= 0 and x <= w and y <= h

def left_traverse(img, x, y):
    current = x
    while(__check_bound(img, x, current) and img[y][current] > 140):
        current -= 1
    return current

def right_traverse(img, x, y):
    current = x
    while(__check_bound(img, x, current) and img[y][current] > 140):
        current += 1
    return current

def up_traverse(img, x, y):
    current = y
    while(__check_bound(img, x, current) and img[current][x] > 140):
        current -= 1
    return current

def down_traverse(img, x, y):
    current = y
    while(__check_bound(img, x, current) and img[current][x] > 140):
        current += 1
    return current
