from Tkinter import *
from PIL import Image, ImageTk

class CanvasCroppable:
    def __init__(self):
        self.rect = None
        self.crop_x0 = 0
        self.crop_y0 = 0
        self.crop_x1 = 0
        self.crop_y1 = 0
        self.crop_view = None
        self.move = False

    def start_paper_crop(self):
        if self.rect != None:
            self.canvas.delete(self.rect)
        self.rect = None
        self.crop_x0 = 0
        self.crop_y0 = 0
        self.crop_x1 = 0
        self.crop_y1 = 0
        self.crop_view = None
        self.move = False

        self.canvas.bind( "<Button-1>", self.__start_crop )
        self.canvas.bind( "<ButtonRelease-1>", self.__end_crop )
        self.canvas.bind( "<Motion>", self.__do_crop )

    def end_paper_crop(self):
        self.canvas.unbind( "<Button-1>")
        self.canvas.unbind( "<ButtonRelease-1>")
        self.canvas.unbind( "<Motion>")
        paperProcessor.crop_page(self.images[self.current_page-1], self.crop_x1, self.crop_y1, self.crop_x0, self.crop_y0)
        self.__load_canvas_image(self.current_page - 1)
        
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

    def __do_crop(self, event):
        if self.move:
            #Translate mouse screen x1,y1 coordinates to canvas coordinates
            self.crop_x1 = self.canvas.canvasx(event.x)
            self.crop_y1 = self.canvas.canvasy(event.y)
            #Modify rectangle x1, y1 coordinates
            self.canvas.coords(self.crop_view, self.crop_x0, self.crop_y0,
                          self.crop_x1, self.crop_y1)

    def __end_crop(self, event):
        self.move = False
        #Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.crop_x1 = self.canvas.canvasx(event.x)
        self.crop_y1 = self.canvas.canvasy(event.y)
        #Modify rectangle x1, y1 coordinates (final)
        self.canvas.coords(self.crop_view, self.crop_x0, self.crop_y0,
                      self.crop_x1, self.crop_y1)
