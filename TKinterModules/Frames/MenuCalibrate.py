from Tkinter import *
from ..AppFrame import AppFrame

class MenuCalibrationFrame(AppFrame):
    def __init__(self, parent, row, column, rowspan, columnspan, sticky):
        AppFrame.__init__(self, parent, row, column, rowspan, columnspan, sticky)
        Label(self.frame, text="Calibration Menu").pack(padx=5, pady=5, fill=X)

    def create_button(self, button_id, title, callback, padx = 0, pady = 0, Show=False):
        self.buttons[button_id] = {
            'node': Button(self.frame, text=title, command=callback),
            'padx': padx,
            'pady': pady
        }
        if Show: self.buttons[button_id]['node'].pack(padx=padx, pady=pady, fill=X)

    def start_region_capture(self):
        self.buttons["startCropPaper"]['node'].pack_forget()
        self.buttons["startMark"]['node'].pack_forget()
        self.buttons["endMark"]['node'].pack(padx=self.buttons["endMark"]['padx'], pady=self.buttons["endMark"]['pady'], fill=X)
        self.buttons["startCropPaper"]['node'].pack(padx=self.buttons["startCropPaper"]['padx'], pady=self.buttons["startCropPaper"]['pady'], fill=X)

    def end_region_capture(self):
        self.buttons["startCropPaper"]['node'].pack_forget()
        self.buttons["endMark"]['node'].pack_forget()
        self.buttons["startMark"]['node'].pack(padx=self.buttons["startMark"]['padx'], pady=self.buttons["startMark"]['pady'], fill=X)
        self.buttons["startCropPaper"]['node'].pack(padx=self.buttons["startCropPaper"]['padx'], pady=self.buttons["startCropPaper"]['pady'], fill=X)

    def start_paper_crop(self):
        self.buttons["startMark"]['node'].pack_forget()
        self.buttons["startCropPaper"]['node'].pack_forget()
        self.buttons["endCropPaper"]['node'].pack(padx=self.buttons["endCropPaper"]['padx'], pady=self.buttons["endCropPaper"]['pady'], fill=X)
        self.buttons["startMark"]['node'].pack(padx=self.buttons["startMark"]['padx'], pady=self.buttons["startMark"]['pady'], fill=X)

    def end_paper_crop(self):
        self.buttons["startMark"]['node'].pack_forget()
        self.buttons["endCropPaper"]['node'].pack_forget()
        self.buttons["startCropPaper"]['node'].pack(padx=self.buttons["startCropPaper"]['padx'], pady=self.buttons["startCropPaper"]['pady'], fill=X)
        self.buttons["startMark"]['node'].pack(padx=self.buttons["startMark"]['padx'], pady=self.buttons["startMark"]['pady'], fill=X)
