from Tkinter import *
from PIL import Image, ImageTk
from tkFileDialog import askopenfilename

from Modules import paperProcessor
from ..FlipperFrame import FlipperFrame
from ..Canvas import AppCanvas
from ..CanvasCroppable import CanvasCroppable
from ..CanvasChopable import CanvasChopable

class PageView(FlipperFrame, AppCanvas, CanvasCroppable, CanvasChopable):
    def __init__(self, app, parent, row, column, rowspan, columnspan, sticky):
        FlipperFrame.__init__(self, app, parent, row, column, rowspan, columnspan, sticky)
        AppCanvas.__init__(self, parent, row, column, rowspan, columnspan, sticky)
        CanvasCroppable.__init__(self)
        CanvasChopable.__init__(self)
        self.imgCurrent = None

    def init_load_paper(self):
        FullPath = askopenfilename(parent=self.app.root, initialdir="C:/",title='Choose Paper')
        FileName = FullPath.split("/")[-1]
        self.pages = sorted(paperProcessor.load_paper(FullPath, FileName), key = lambda x:int(x.split("/")[-1].split(".")[0]))

        self.__init_viewer()

        self.canvas.configure(width=self.imgCurrent.width(), height=self.imgCurrent.height())
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        return FileName.split(".")[0]

    def init_mark_paper(self, root_path, questions):
        self.pages = []
        for question in questions:
            self.pages.append({
                "name": question["name"],
                "page_start": question["page_start"],
                "page_end": question["page_end"],
                "x_start": question["x_start"],
                "x_end": question["x_end"],
                "image": paperProcessor.clobber_image(root_path, question["name"], question["page_start"], question["x_start"], question["page_end"], question["x_end"])
            })
        self.__init_viewer()

    def __init_viewer(self):
        self.strCurrentPage.set(1)
        self.strTotalPage.set(len(self.pages))
        self.__load_page(int(self.strCurrentPage.get()) - 1)


    def next_page(self):
        intCurrentPage = int(self.strCurrentPage.get())
        intMaxPage = int(self.strTotalPage.get())
        if intCurrentPage < intMaxPage:
            self.strCurrentPage.set(intCurrentPage + 1)
            self.__load_page(int(self.strCurrentPage.get()) - 1)

    def prev_page(self):
        intCurrentPage = int(self.strCurrentPage.get())
        if intCurrentPage > 1:
            self.strCurrentPage.set(intCurrentPage - 1)
            self.__load_page(int(self.strCurrentPage.get()) - 1)

    def __load_page(self, pageIndex):
        try:
            self.imgCurrent = ImageTk.PhotoImage(Image.open(self.pages[pageIndex]))
        except Exception:
            self.imgCurrent = ImageTk.PhotoImage(Image.fromarray(self.pages[pageIndex]["image"]))

        self.app.root.__imgCurrent = self.imgCurrent
        self.canvas.create_image(0, 0, image=self.imgCurrent, anchor=NW)
