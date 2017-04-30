import sys
from Tkinter import *
from Modules import paperProcessor

def main():
    target_pdf = sys.argv[1]
    root = Tk()
    root.state('zoomed')
    text = "HAHAHAHA"
    w = Label(root, text = text)
    w.pack()
    root.mainloop()

main()
