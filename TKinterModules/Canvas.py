from Tkinter import *
from PIL import Image, ImageTk

class AppCanvas:
    def __init__(self, parent, row, column, rowspan, columnspan, sticky):
        self.xsb = Scrollbar(parent, orient="horizontal")
        self.ysb = Scrollbar(parent, orient="vertical")
        self.canvas = Canvas(parent, bd=2, xscrollcommand=self.xsb.set, yscrollcommand=self.ysb.set)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        self.xsb.grid(row=rowspan-1, column=0, columnspan=columnspan, sticky="ews")
        self.ysb.grid(row=0, column=columnspan-1, rowspan=rowspan, sticky="nse")

        self.xsb.config(command=self.canvas.xview)
        self.ysb.config(command=self.canvas.yview)

        self.canvas.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)

        self.xsb.lift()
        self.ysb.lift()
