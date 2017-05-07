from Tkinter import *
from PIL import Image, ImageTk

class CanvasChopable:
    def __init__(self):
        self.coordCurrentRegion = [0, 0]
        self.markCurrentRegion = {}

    def start_region_capture(self):
        self.coordCurrentRegion = [0, 0]
        self.canvas.bind( "<Button-1>", self.__record_point )

    def end_region_capture(self):
        self.canvas.unbind( "<Button-1>")
        print self.markCurrentRegion
        for index, marker in enumerate(self.markCurrentRegion.keys()):
            self.canvas.delete(self.markCurrentRegion[marker])
        self.markCurrentRegion = {}

    def mark(self, page, y, visible = False):
            if str(page)+","+str(y) in self.markCurrentRegion.keys():
                self.canvas.delete(self.markCurrentRegion[str(page)+","+str(y)])
            else:
                self.markCurrentRegion[str(page)+","+str(y)] = self.canvas.create_line(0, y, self.imgCurrent.width(), y, fill="red", dash=(4,4))

    def __record_point(self, event):
        coordPage = (event.y, int(self.strCurrentPage.get()) - 1)
        if self.coordCurrentRegion[0] == 0:
            self.coordCurrentRegion[0] = coordPage
            self.mark(coordPage[1], coordPage[0])
        elif self.coordCurrentRegion[1] == 0:
            self.coordCurrentRegion[1] = coordPage
            self.mark(coordPage[1], coordPage[0])

        print self.coordCurrentRegion
