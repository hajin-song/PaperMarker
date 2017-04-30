import sys
import ghostscript
import cv2

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

def main():
    target_pdf = sys.argv[1]
    gs_args = ["-q", "-dNOPAUSE", "-dBATCH", "-dNOPROMPT", "-dNOSAFER", "-sDEVICE=png16m", "-sOutputFile=" + PROCESSED_IMG_PATH +"/target_img-%d.png", target_pdf]
    ghostscript.Ghostscript(*gs_args)

    img = cv2.imread(PROCESSED_IMG_PATH + '/target_img-1.png', 0)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
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

    cv2.imwrite('./image_marked.png', img_rgb)
    cv2.imwrite('./image_processed.png', img)
main()
