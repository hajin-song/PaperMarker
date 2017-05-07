import sys
import ghostscript
import cv2
import os
import numpy as np

from Modules.TemplateMatcher import templateMatcher
from Modules.Traverser import traverser
CORNER_SYMBOL_WIDTH = 5 # 5mm
CORNER_SYMBOL_HEIGHT = 5 # 5mm

LINE_THCIKNESS = 1 # 1mm

SCAN_BUBBLE_WIDTH = 5 # 5mm
SCAN_BUBBLE_HEIGHT = 5 # 5mm

TEMPLATE_TOP_RIGHT = cv2.imread("./images/templates/top-right-corner.png", 0)
TEMPLATE_TOP_LEFT = cv2.imread("./images/templates/top-left-corner.png", 0)
TEMPLATE_BOTTOM_RIGHT = cv2.imread("./images/templates/bottom-right-corner.png", 0)
TEMPLATE_BOTTOM_LEFT = cv2.imread("./images/templates/bottom-left-corner.png", 0)

TEMPLATE = {
    "top_right": TEMPLATE_TOP_RIGHT,
    "top_left": TEMPLATE_TOP_LEFT,
    "bottom_right": TEMPLATE_BOTTOM_RIGHT,
    "bottom_left": TEMPLATE_BOTTOM_LEFT
}

PROCESSED_IMG_PATH = "./images/processed"

def __extract_border_marker(top_right, top_left, bottom_right, bottom_left):
    top_right_x_coord = sorted(top_right.keys())[-1]
    top_left_x_coord = sorted(top_left.keys())[0]
    bottom_right_x_coord = sorted(bottom_right.keys())[-1]
    bottom_left_x_coord = sorted(bottom_left.keys())[0]

    top_right_y_coord = sorted(top_right[top_right_x_coord].keys())[0]
    top_left_y_coord = sorted(top_left[top_left_x_coord].keys())[0]
    bottom_left_y_coord = sorted(bottom_right[bottom_right_x_coord].keys())[-1]
    bottom_right_y_coord = sorted(bottom_left[bottom_left_x_coord].keys())[-1]

    return {
        "top_right": [top_right_x_coord, top_right_y_coord],
        "top_left": [top_left_x_coord, top_left_y_coord],
        "bottom_right": [bottom_right_x_coord, bottom_right_y_coord],
        "bottom_left": [bottom_left_x_coord, bottom_left_y_coord]
    }

def __find_border(img, top_right, top_left, bottom_right, bottom_left):
    top_right = [traverser.left_traverse(img, top_right[0], top_right[1]), traverser.down_traverse(img, top_right[0], top_right[1])]
    top_left = [traverser.right_traverse(img, top_left[0], top_left[1]), traverser.down_traverse(img, top_left[0], top_left[1])]
    bottom_right = [traverser.left_traverse(img, bottom_right[0], bottom_right[1]), traverser.up_traverse(img, bottom_right[0], bottom_right[1])]
    bottom_left = [traverser.right_traverse(img, bottom_left[0], bottom_left[1]), traverser.up_traverse(img, bottom_left[0], bottom_left[1])]
    return {
        "top_right": top_right,
        "top_left": top_left,
        "bottom_right": bottom_right,
        "bottom_left": bottom_left
    }

def load_paper(target_path, target_pdf):
    print target_pdf
    file_name = target_pdf.split("/")[::-1][0].split(".")[0]
    target_directory = PROCESSED_IMG_PATH + "/" + file_name
    if not os.path.exists(target_directory): os.mkdir(target_directory)


    gs_args = ["-q", "-dNOPAUSE", "-dBATCH", "-dNOPROMPT", "-dNOSAFER", "-sDEVICE=png16m", "-sOutputFile=" + target_directory +"/%d.png", target_path]
    ghostscript.Ghostscript(*gs_args)

    images = os.listdir(target_directory)
    images = [image for image in images if image.endswith(".png")]
    result_image_path = []

    for image in images:
        result_image_path.append(target_directory + '/' + image)
        img = cv2.imread(target_directory + '/' + image, 0)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        try:
            top_right = templateMatcher.detectSymbols(img, img_rgb, TEMPLATE_TOP_RIGHT)
            top_left = templateMatcher.detectSymbols(img, img_rgb, TEMPLATE_TOP_LEFT)
            bottom_right = templateMatcher.detectSymbols(img, img_rgb, TEMPLATE_BOTTOM_RIGHT)
            bottom_left = templateMatcher.detectSymbols(img, img_rgb, TEMPLATE_BOTTOM_LEFT)

            corner_symbols = __extract_border_marker(top_right, top_left, bottom_right, bottom_left)

            for symbol in corner_symbols.keys():
                coord = corner_symbols[symbol]
                w,h = TEMPLATE[symbol].shape[::-1]
                cv2.rectangle(img_rgb, tuple(coord), (coord[0] + w, coord[1] + h), (255,0,0), 1)
                templateMatcher.removeDetected(img, coord[1], coord[0], w, h)


            border_pos = __find_border(img, corner_symbols["top_right"], corner_symbols["top_left"], corner_symbols["bottom_right"], corner_symbols["bottom_left"])
            for pos in border_pos:
                coord = border_pos[pos]
                cv2.rectangle(img_rgb, tuple(coord), (coord[0] + 1, coord[1] + 1), (0,255,0), 1)
        except Exception:
            continue
        cv2.imwrite(target_directory + '/' + image, img)
    return result_image_path

def crop_page(img_name, x0, y0, x1, y1):
    if x0 == x1 and y0==y1: return
    print img_name
    try:
        img = cv2.imread(img_name)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        img = cv2.imread(img_name)
    print img
    img = np.asarray(img)

    if x0 <= x1:
        x_min = x0
        x_max = x1
    else:
        x_max = x1
        x_max = x0

    if y0 <= y1:
        y_min = y0
        y_max = y1
    else:
        y_min = y1
        y_max = y0

    print x_min, y_min, x_max, y_max
    img = img[int(y_min):int(y_max), int(x_min):int(x_max)]
    print img
    cv2.imwrite(img_name, img)

def clobber_image(target_directory, id, img_one, x_one, img_two, x_two):
    crop_dir = target_directory + "/" + "questions"
    if not os.path.exists(crop_dir): os.mkdir(crop_dir)

    img_one = target_directory + "/" + str(int(img_one)+1) + ".png"
    img_two = target_directory + "/" + str(int(img_two)+1) + ".png"
    try:
        img_one_np = cv2.imread(img_one)
        img_one_np = cv2.cvtColor(img_one_np, cv2.COLOR_BGR2GRAY)
        img_two_np = cv2.imread(img_two)
        img_two_np = cv2.cvtColor(img_two_np, cv2.COLOR_BGR2GRAY)
    except:
        img_one_np = cv2.imread(img_one)
        img_two_np = cv2.imread(img_two)
    w,h = img_one_np.shape[::-1]

    if img_one == img_two:
        cv2.imwrite(crop_dir+"/"+str(id)+".png", img_one_np[int(x_one):int(x_two), :])
        return img_one_np[int(x_one):int(x_two), :]
    else:
        img_one_np[int(x_one):, :]
        img_two_np[:int(x_two), :]
        cv2.imwrite(crop_dir+"/"+str(id)+".png", img_one_np[int(x_one):int(x_two), :])
        return np.concatenate((img_one_np, img_two_np), axis=1)
