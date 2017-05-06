from Tkinter import *

class AppFrame:
    def __init__(self, parent, row, column, rowspan, columnspan, sticky):
        self.row = row
        self.column = column
        self.rowspan = rowspan
        self.columnspan = columnspan
        self.sticky = sticky

        self.buttons = {}

        self.parent = parent
        self.frame = Frame(self.parent, bd=2, relief = RAISED, bg="green")

    def show(self):
        self.frame.grid(column=self.column, row=self.row, rowspan=self.rowspan, columnspan=self.columnspan, sticky=self.sticky)

    def hide(self):
        self.frame.grid_forget()

    def create_button(self, button_id, title, callback, padx = 0, pady = 0, Show=False):
        self.buttons[button_id] = {
            'node': Button(self.frame, text=title, command=callback),
            'padx': padx,
            'pady': pady
        }
        self.buttons[button_id]['node'].pack(
            padx=self.buttons[button_id]['padx'],
            pady=self.buttons[button_id]['pady'],
            side=LEFT
        )

    def bind_action(self, button_id, action, callback):
        self.buttons[button_id]['node'].bind(action, callback)

    def unbind_action(self, button_id, action):
        self.buttons[button_id]['node'].unbind(action)
