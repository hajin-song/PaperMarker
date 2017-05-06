from Tkinter import *
import ttk
from Modules import paperProcessor
from PIL import Image, ImageTk
from tkFileDialog import askopenfilename

class PageView:
    def __init__(self, root, parent, row, column, rowspan, columnspan, sticky):
        self.root = root
        self.images = []
        self.current_page = 0
        self.page_count = 0

        self.xsb = Scrollbar(parent, orient="horizontal")
        self.ysb = Scrollbar(parent, orient="vertical")
        self.canvas = Canvas(parent, bd=0, xscrollcommand=self.xsb.set, yscrollcommand=self.ysb.set)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        self.xsb.grid(row=rowspan-1, column=0, columnspan=columnspan, sticky="ews")
        self.ysb.grid(row=0, column=columnspan-1, rowspan=rowspan, sticky="nse")

        self.xsb.config(command=self.canvas.xview)
        self.ysb.config(command=self.canvas.yview)

        self.canvas.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)

        self.xsb.lift()
        self.ysb.lift()

        self.parent = parent

        # x_start, x_end
        self.current_region = [0, 0]
        self.current_region_mark = []

        self.rect = None
        self.crop_x0 = 0
        self.crop_y0 = 0
        self.crop_x1 = 0
        self.crop_y1 = 0
        self.crop_view = None
        self.move = False

    def load_image(self):
        self.current_page = 0
        self.page_count = 0

        FullPath = askopenfilename(parent=self.root, initialdir="C:/",title='Choose Paper')
        FileName = FullPath.split("/")[-1]
        self.images = paperProcessor.load_paper(FullPath, FileName)

        self.__load_canvas_image(self.current_page)
        self.current_page = 1
        self.page_count = len(self.images)

        self.canvas.configure(width=self.current_image.width(), height=self.current_image.height())
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

    def start_region_capture(self):
        self.current_region = [0, 0]
        self.canvas.bind( "<Button-1>", self.__record_point )

    def end_region_capture(self):
        self.canvas.unbind( "<Button-1>")
        print self.current_region_mark
        for index, marker in enumerate(self.current_region_mark):
            self.canvas.delete(marker)
        self.current_region_mark = []

    def start_paper_crop(self):
        self.canvas.bind( "<Button-1>", self.__start_crop )
        self.canvas.bind( "<ButtonRelease-1>", self.__end_crop )
        self.canvas.bind( "<Motion>", self.__do_crop )

    def end_paper_crop(self):
        if self.rect != None:
            self.canvas.delete(self.rect)
        self.canvas.unbind( "<Button-1>")
        self.canvas.unbind( "<ButtonRelease-1>")
        self.canvas.unbind( "<Motion>")
        paperProcessor.crop_page(self.images[self.current_page-1], self.crop_x1, self.crop_y1, self.crop_x0, self.crop_y0)
        self.__load_canvas_image(self.current_page - 1)

    def __load_canvas_image(self, image_index):
        self.current_image = ImageTk.PhotoImage(Image.open(self.images[image_index]))
        self.root.__curImage = self.current_image
        self.canvas.create_image(0, 0, image=self.current_image, anchor=NW)

    def __start_crop(self, event):
        if self.rect != None:
            self.canvas.delete(self.rect)
        self.move = True
        #Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.crop_x0 = self.canvas.canvasx(event.x)
        self.crop_y0 = self.canvas.canvasy(event.y)
        #Create rectangle
        self.rect = self.canvas.create_rectangle(
            self.crop_x0, self.crop_y0, self.crop_x0, self.crop_y0, dash=(4,4))
        self.crop_view = self.canvas.find_closest(self.crop_x0, self.crop_y0, halo=2)
        print('Rectangle {0} started at {1} {2} {3} {4} '.
              format(self.rect, self.crop_x0, self.crop_y0, self.crop_x0,
                     self.crop_y0))

    def __do_crop(self, event):
        if self.move:
            #Translate mouse screen x1,y1 coordinates to canvas coordinates
            self.crop_x1 = self.canvas.canvasx(event.x)
            self.crop_y1 = self.canvas.canvasy(event.y)
            #Modify rectangle x1, y1 coordinates
            self.canvas.coords(self.crop_view, self.crop_x0, self.crop_y0,
                          self.crop_x1, self.crop_y1)
            print('Rectangle x1, y1 = ', self.crop_x1, self.crop_y1)

    def __end_crop(self, event):
        self.move = False
        #Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.crop_x1 = self.canvas.canvasx(event.x)
        self.crop_y1 = self.canvas.canvasy(event.y)
        #Modify rectangle x1, y1 coordinates (final)
        self.canvas.coords(self.crop_view, self.crop_x0, self.crop_y0,
                      self.crop_x1, self.crop_y1)
        print('Rectangle ended')


    def __record_point(self, event):
        image_x_center = self.current_image.width()/2
        image_y_center = self.current_image.height()/2
        if self.current_region[0] == 0:
            self.current_region[0] = event.y
            self.current_region_mark.append(self.canvas.create_line(0, event.y, self.current_image.width(), event.y, fill="red", dash=(4,4)))
        elif self.current_region[1] == 0:
            self.current_region[1] = event.y
            self.current_region_mark.append(self.canvas.create_line(0, event.y, self.current_image.width(), event.y, fill="red", dash=(4,4)))

        print self.current_region
