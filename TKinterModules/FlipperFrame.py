from Tkinter import *
from AppFrame import AppFrame

class FlipperFrame(AppFrame):
    def __init__(self, app, parent, row, column, rowspan, columnspan, sticky):
        AppFrame.__init__(self, app, parent, row, column, rowspan, columnspan, sticky)

        self.strCurrentPage = StringVar()
        self.strCurrentPage.set("0")
        self.strTotalPage = StringVar()
        self.strTotalPage.set("0")

        self.pages = []

    def set_current_page(self, val):
        self.strCurrentPage.set(str(val))

    def set_total_page(self, val):
        self.strTotalPage.set(str(val))

    def next_page(self):
        currentPage = int(self.strCurrentPage.get())
        maxPage = int(self.strTotalPage.get())
        if currentPage < maxPage:
            self.__unload_page(int(self.strCurrentPage.get()) - 1)
            self.strCurrentPage.set(str(currentPage+1))
            self.__load_page(int(self.strCurrentPage.get()) - 1)

    def prev_page(self):
        currentPage = int(self.strCurrentPage.get())
        if currentPage > 1:
            self.__unload_page(int(self.strCurrentPage.get()) - 1)
            self.strCurrentPage.set(str(currentPage-1))
            self.__load_page(int(self.strCurrentPage.get()) - 1)

    def __unload_page(self, page_index):
        pass
    def __load_page(self, page_index):
        pass
