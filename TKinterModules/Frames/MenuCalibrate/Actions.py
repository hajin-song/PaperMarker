from Tkinter import *
from ../../AppFrame import AppFrame

class Actions(AppFrame):
    def __init__(self, app, row, column, rowspan, columnspan, sticky):
        AppFrame.__init__(self, app, row, column, rowspan, columnspan, sticky)
