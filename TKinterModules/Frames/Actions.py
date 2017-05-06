from Tkinter import *
from ..AppFrame import AppFrame

class ActionFrame(AppFrame):
    def __init__(self, root, parent, row, column, rowspan, columnspan, sticky):
        AppFrame.__init__(self, root, parent, row, column, rowspan, columnspan, sticky)
