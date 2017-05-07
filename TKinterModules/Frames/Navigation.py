from Tkinter import *
from ..AppFrame import AppFrame

class Navigation(AppFrame):
    def __init__(self, app, parent, row, column, rowspan, columnspan, sticky):
        AppFrame.__init__(self, app, parent, row, column, rowspan, columnspan, sticky)

        self.currentPage = StringVar()
        self.currentPage.set("0")
        self.totalPage = StringVar()
        self.totalPage.set("0")

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.buttons["prevPage"] = Button(self.frame, text="<")
        self.buttons["prevPage"].pack(padx=10, pady=5, side=LEFT, expand=True)
        Label(self.frame, textvariable=self.currentPage).pack(padx=5, pady=5, side=LEFT, expand=True)
        Label(self.frame, text=" of ").pack(padx=5, pady=5, side=LEFT, expand=True)
        Label(self.frame, textvariable=self.totalPage).pack(padx=5, pady=5, side=LEFT, expand=True)
        self.buttons["nextPage"] = Button(self.frame, text=">")
        self.buttons["nextPage"].pack(padx=10, pady=5, side=LEFT, expand=True)

    def bind_action(self, button_id, action, callback):
        self.buttons[button_id].bind(action, callback)

    def unbind_action(self, button_id, action):
        self.buttons[button_id].unbind(action)

    def set_current_page(self, val):
        self.currentPage.set(str(val))

    def set_total_page(self, val):
        self.totalPage.set(str(val))

    def next_page(self):
        cur_page = int(self.currentPage.get())
        max_page = int(self.totalPage.get())
        if cur_page < max_page:
            self.currentPage.set(str(cur_page+1))

    def prev_page(self):
        cur_page = int(self.currentPage.get())
        max_page = int(self.totalPage.get())
        if cur_page > 1:
            self.currentPage.set(str(cur_page-1))
