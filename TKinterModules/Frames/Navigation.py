from Tkinter import *
from ..FlipperFrame import FlipperFrame

class Navigation(FlipperFrame):
    def __init__(self, app, parent, row, column, rowspan, columnspan, sticky):
        FlipperFrame.__init__(self, app, parent, row, column, rowspan, columnspan, sticky)

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.buttons["prevPage"] = { "node": Button(self.frame, text="<") }
        self.buttons["prevPage"]["node"].pack(padx=10, pady=5, side=LEFT, expand=True)
        Label(self.frame, textvariable=self.strCurrentPage).pack(padx=5, pady=5, side=LEFT, expand=True)
        Label(self.frame, text=" of ").pack(padx=5, pady=5, side=LEFT, expand=True)
        Label(self.frame, textvariable=self.strTotalPage).pack(padx=5, pady=5, side=LEFT, expand=True)
        self.buttons["nextPage"] = { "node": Button(self.frame, text=">") }
        self.buttons["nextPage"]["node"].pack(padx=10, pady=5, side=LEFT, expand=True)
