import sys
from Tkinter import *
from Modules import paperProcessor
from Modules import Calibration
from PIL import Image, ImageTk
from tkFileDialog import askopenfilename

from TKinterModules.Frames.Actions import ActionFrame
from TKinterModules.Frames.MenuCalibrate import MenuCalibrationFrame
from TKinterModules.Frames.MenuMark import MenuMarkFrame
from TKinterModules.Frames.Navigation import Navigation

from TKinterModules.Components.PageView import PageView

APP_DIVIDER_LINE_WIDTH = 5

Frame = LabelFrame

class PaperMarker:
    def __init__(self, root):
        self.frames = {}
        self.env = {}
        self.questions = []

        self.root = root
        self.root.state('zoomed')
        self.root.update()

        self.frames["main"] = Frame(root, bd=2, relief=SUNKEN)
        self.frames["main"].pack(fill=BOTH, expand=1)

        for i in range(0, 5):
            self.frames["main"].columnconfigure(i, weight=1)
            self.frames["main"].rowconfigure(i, weight=1)

        self.frames["buttons"] = ActionFrame(self, self.frames["main"], 5, 0, 1, 4, (S,E,W,N))
        self.frames["buttons"].show()

        self.frames["menuCalibrate"] = MenuCalibrationFrame(self, self.frames["main"], 0, 4, 5, 1, (S,E,W,N))
        self.frames["menuMark"] =  MenuMarkFrame(self, self.frames["main"], 0, 4, 5, 1, (S,E,W,N))

        self.frames["flipper"] = Navigation(self, self.frames["main"], 5, 4, 1, 1, (S,E,W,N))
        self.frames["flipper"].show()

        self.pageView = PageView(self, self.frames["main"], 0, 0, 5, 4, (S,E,W,N))

    def init_load_paper(self):
        self.env["EXAM_ROOT_PATH"] = self.pageView.load_image()
        self.__load_paper_pages()
        self.__set_as_calibrate_mode()

    def next_page(self, event):
        self.frames["flipper"].next_page()
        self.pageView.next_page()

    def prev_page(self, event):
        self.frames["flipper"].prev_page()
        self.pageView.prev_page()

    def get_questions(self):
        result = self.frames["menuCalibrate"].get_questions()
        Calibration.save_calibration(self.env["EXAM_ROOT_PATH"], result)
        print result

    def show_question_region(self, coords, visible):
        for coord in coords:
            self.pageView.mark(coord[1], coord[0], visible)

    def start_paper_crop(self):
        self.frames['menuCalibrate'].start_paper_crop()
        self.frames['menuCalibrate'].disable_button("startMark")
        for button in self.frames['buttons'].buttons:
            self.frames['buttons'].buttons[button]['node'].config(state = DISABLED)
        self.pageView.start_paper_crop()

    def end_paper_crop(self):
        self.frames['menuCalibrate'].end_paper_crop()
        self.frames['menuCalibrate'].enable_button("startMark")
        for button in self.frames['buttons'].buttons:
            self.frames['buttons'].buttons[button]['node'].config(state = NORMAL)
        self.pageView.end_paper_crop()

    def start_region_capture(self):
        self.frames["menuCalibrate"].start_region_capture()
        self.pageView.start_region_capture()
        self.frames['menuCalibrate'].disable_button("startCropPaper")
        for button in self.frames['buttons'].buttons:
            self.frames['buttons'].buttons[button]['node'].config(state = DISABLED)

    def end_region_capture(self):
        region = tuple(self.pageView.current_region)
        self.frames["menuCalibrate"].end_region_capture(region)
        self.pageView.end_region_capture()

        self.frames['menuCalibrate'].enable_button("startCropPaper")
        for button in self.frames['buttons'].buttons:
            self.frames['buttons'].buttons[button]['node'].config(state = NORMAL)

    def __load_paper_pages(self):
        self.frames["flipper"].set_current_page(self.pageView.current_page)
        self.frames["flipper"].set_total_page(self.pageView.page_count)

    def __set_as_mark_mode(self):
        self.frames["menuCalibrate"].hide()
        self.frames["menuMark"].show()

    def __set_as_calibrate_mode(self):
        self.frames["menuCalibrate"].show()
        self.frames["menuMark"].hide()

def main():
    root = Tk()
    app = PaperMarker(root)

    app.frames["buttons"].create_button("loadPaper", "Load New Paper",  app.init_load_paper, 10, 10)

    app.frames["menuCalibrate"].create_button("saveExamSetting", "Export Current Setting",  app.get_questions, 10, 10, True)
    app.frames["menuCalibrate"].create_button("startCropPaper", "Crop to Questions", app.start_paper_crop, 10, 10, True)
    app.frames["menuCalibrate"].create_button("endCropPaper", "End Crop", app.end_paper_crop, 10, 10)

    app.frames["menuCalibrate"].create_button("startMark", "Start Question Capture", app.start_region_capture, 10, 10, True)
    app.frames["menuCalibrate"].create_button("endMark", "End Question Capture",app.end_region_capture, 10, 10)

    app.frames["flipper"].bind_action("nextPage", "<Button-1>", app.next_page)
    app.frames["flipper"].bind_action("prevPage", "<Button-1>", app.prev_page)

    root.mainloop()

main()
