from Tkinter import *
from ..AppFrame import AppFrame

class MenuMarkFrame(AppFrame):
    def __init__(self, app, parent, row, column, rowspan, columnspan, sticky):
        AppFrame.__init__(self, app, parent, row, column, rowspan, columnspan, sticky)
        Label(self.frame, text="Mark Menu").pack(padx=5, pady=5, fill=X)
