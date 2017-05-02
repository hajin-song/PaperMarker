import sys
from Tkinter import *
import ttk
from Modules import paperProcessor

APP_DIVIDER_LINE_WIDTH = 5

class PaperMarker:
    def __init__(self, root):
        self.labels = {}
        self.chkButtons = {}
        self.buttons = {}
        self.input = {}

        self.root = root
        self.root.state('zoomed')
        self.root.update()
        self.content = ttk.Frame(root)
        self.frame = ttk.Frame(self.content, borderwidth=5, relief="sunken")
        self.buttonFrame = ttk.Frame(self.content)

        self.labels["name"] = ttk.Label(self.content, text="Name")
        self.input["name"] = ttk.Entry(self.content)


        self.content.grid(column = 0, row = 0, sticky=(N, S, E, W))
        self.frame.grid(column = 0, row = 0, columnspan = 3, rowspan = 2, sticky=(N, S, E, W))
        self.buttonFrame.grid(column = 0, row = 2, columnspan = 3, rowspan = 2, sticky=(N, S, E, W))

        self.labels["name"].grid(column=3, row=0, columnspan=2, stick=(N, W), padx=5)
        self.input["name"].grid(column=3, row=1, columnspan=2, sticky=(N, E, W), pady=5, padx=5)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=3)
        self.content.columnconfigure(1, weight=3)
        self.content.columnconfigure(2, weight=1)
        self.content.columnconfigure(3, weight=1)
        self.content.columnconfigure(4, weight=1)
        self.content.columnconfigure(5, weight=1)
        self.content.rowconfigure(1, weight=1)


    def create_button(self, title, column, row, columnspan, rowspan, padx = 0, pady = 0):
        new_button = ttk.Button(self.buttonFrame, text=title)
        new_button.grid(column = column, row = row, columnspan = columnspan, padx = padx, pady = pady)
        self.buttons[title] = new_button

    def get_canvas(self):
        return self.canvas

    def get_height(self):
        return self.root.winfo_height()

    def get_width(self):
        return self.root.winfo_width()

    def get_geometry(self):
        return self.root.winfo_geometry()



def main():
    root = Tk()
    app = PaperMarker(root)

    print app.get_height()
    print app.get_width()
    print app.get_geometry()
    app.create_button("test", 0, 0, 2, 2, 10, 10)
    app.create_button("test1", 2, 0, 2, 2, 10, 10)
    app.create_button("test2", 4, 0, 2, 2, 10, 10)
    app.create_button("test3", 6, 0, 2, 2, 10, 10)
    root.mainloop()

main()
