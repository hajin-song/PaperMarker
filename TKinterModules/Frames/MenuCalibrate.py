from Tkinter import *
from ..AppFrame import AppFrame

class MenuCalibrationActions(AppFrame):
    def __init__(self, app, parent, row, column, rowspan, columnspan, sticky):
        AppFrame.__init__(self, app, parent, row, column, rowspan, columnspan, sticky, 'red')
        Label(self.frame, text="Calibration Menu").pack(padx=5, pady=5, fill=X)

    def create_button(self, button_id, title, callback, padx = 0, pady = 0, Show=False):
        self.buttons[button_id] = {
            'node': Button(self.frame, text=title, command=callback),
            'padx': padx,
            'pady': pady
        }
        if Show: self.buttons[button_id]['node'].pack(padx=padx, pady=pady, fill=X)

    def show(self):
        self.frame.pack(fill=X)

    def hide(self):
        self.frame.pack_forget()

    def start_region_capture(self):
        self.buttons["startMark"]['node'].pack_forget()
        self.buttons["startCropPaper"]['node'].pack_forget()
        self.buttons["startCropPaper"]['node'].pack(padx=self.buttons["startCropPaper"]['padx'], pady=self.buttons["startCropPaper"]['pady'], fill=X)
        self.buttons["endMark"]['node'].pack(padx=self.buttons["endMark"]['padx'], pady=self.buttons["endMark"]['pady'], fill=X)

    def end_region_capture(self):
        self.buttons["startCropPaper"]['node'].pack_forget()
        self.buttons["endMark"]['node'].pack_forget()
        self.buttons["startCropPaper"]['node'].pack(padx=self.buttons["startCropPaper"]['padx'], pady=self.buttons["startCropPaper"]['pady'], fill=X)
        self.buttons["startMark"]['node'].pack(padx=self.buttons["startMark"]['padx'], pady=self.buttons["startMark"]['pady'], fill=X)

    def start_paper_crop(self):
        self.buttons["startMark"]['node'].pack_forget()
        self.buttons["startCropPaper"]['node'].pack_forget()
        self.buttons["endCropPaper"]['node'].pack(padx=self.buttons["endCropPaper"]['padx'], pady=self.buttons["endCropPaper"]['pady'], fill=X)
        self.buttons["startMark"]['node'].pack(padx=self.buttons["startMark"]['padx'], pady=self.buttons["startMark"]['pady'], fill=X)

    def end_paper_crop(self):
        self.buttons["startMark"]['node'].pack_forget()
        self.buttons["endCropPaper"]['node'].pack_forget()
        self.buttons["startCropPaper"]['node'].pack(padx=self.buttons["startCropPaper"]['padx'], pady=self.buttons["startCropPaper"]['pady'], fill=X)
        self.buttons["startMark"]['node'].pack(padx=self.buttons["startMark"]['padx'], pady=self.buttons["startMark"]['pady'], fill=X)

class MenuCalibrationListItemAnnotator(Toplevel):
    def __init__(self, root, cur_name, cur_criterias = []):
        Toplevel.__init__(self, root)
        self.transient(root)
        self.title("Annotator")

        self.parent = root

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body, cur_name, cur_criterias)
        body.pack(padx=5, pady=5)
        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (root.winfo_rootx()/2,
                                  root.winfo_rooty()/2))

        self.initial_focus.focus_set()

        self.wait_window(self)

    def body(self, root, cur_name, cur_criterias):
        self.root = root
        self.cur_row = 0
        self.criteriaEntries = []
        Label(root, text="Question Name:").grid(row=self.cur_row)
        self.name = Entry(root)
        self.name.insert(10, cur_name)
        self.name.grid(row=self.cur_row, column=1)
        self.cur_row += 1
        Button(root, text="Add Criteria", command=self.__add_field).grid(row=self.cur_row)
        for criteria in cur_criterias:
            self.cur_row += 1
            Label(root, text="Criteria " + str(self.cur_row)).grid(row=self.cur_row)
            crit = Entry(root)
            crit.insert(10, criteria)
            crit.grid(row=self.cur_row, column=1)
            self.criteriaEntries.append(crit)
        return self.name # initial focus
    #
    # command hooks
    def buttonbox(self):
        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        return 1 # override

    def apply(self):
        name = self.name.get()
        criterias = []
        for criteria in self.criteriaEntries:
            criterias.append(criteria.get())
        self.result = name, criterias

    def __add_field(self):
        self.cur_row += 1
        Label(self.root, text="Criteria " + str(self.cur_row)).grid(row=self.cur_row)
        crit = Entry(self.root)
        crit.insert(10, "")
        crit.grid(row=self.cur_row, column=1)
        self.criteriaEntries.append(crit)

class MenuCalibrationListItem(AppFrame):
    def __init__(self, app, parent, row, column, rowspan, columnspan, sticky, name, coord):
        AppFrame.__init__(self, app, parent, row, column, rowspan, columnspan, sticky, 'yellow')
        self.frame.pack(fill=X, padx=10, pady=10)

        self.question_name = StringVar()
        self.question_name.set(name)
        self.visible = False
        self.identifier = name
        self.coord = coord
        self.criterias = []

        Label(self.frame, textvariable=self.question_name).pack(padx=5, pady=5, side=LEFT, expand=True)
        self.buttons["Toggle"] = Button(self.frame, command=self.__toggle, text="Toggle").pack(padx=5, pady=5, side=LEFT, expand=True)
        self.buttons["Annotate"] = Button(self.frame, command=self.__annotate, text="Annotate").pack(padx=5, pady=5, side=LEFT, expand=True)
        self.buttons["Delete"] = Button(self.frame, command=self.__delete, text="Delete").pack(padx=5, pady=5, side=LEFT, expand=True)
        self.annotator = MenuCalibrationListItemAnnotator(self.app.root, self.question_name.get(), self.criterias)
        name, self.criterias =  self.annotator.result
        self.question_name.set(name)

    def __toggle(self):
        self.app.show_question_region(self.coord, self.visible)
        self.visible = not self.visible

    def __annotate(self):
        self.annotator = MenuCalibrationListItemAnnotator(self.app.root, self.question_name.get(), self.criterias)
        name, self.criterias =  self.annotator.result
        self.question_name.set(name)

    def __delete(self):
        self.frame.pack_forget()
        self.parent.delete_question(self.identifier)

class MenuCalibrationList(AppFrame):
    def __init__(self, app, parent, row, column, rowspan, columnspan, sticky):
        AppFrame.__init__(self, app, parent, row, column, rowspan, columnspan, sticky, 'yellow')
        Label(self.frame, text="asdasd Menu").pack(padx=5, pady=5, fill=X)
        self.questions = {}

    def create_button(self, button_id, title, callback, padx = 0, pady = 0, Show=False):
        self.buttons[button_id] = {
            'node': Button(self.frame, text=title, command=callback),
            'padx': padx,
            'pady': pady
        }
        if Show: self.buttons[button_id]['node'].pack(padx=padx, pady=pady, fill=X)

    def show(self):
        self.frame.pack(fill=X)

    def hide(self):
        self.frame.pack_forget()

    def end_region_capture(self, region):
        self.__add_question(region)

    def delete_question(self, index):
        print self.questions
        self.questions.pop(str(index), None)

    def __add_question(self, region):
        new_q = MenuCalibrationListItem(self.app, self.frame, 0, 0, 0, 0, (E,W), len(self.questions) + 1, region)
        self.questions[str(len(self.questions) + 1)] = new_q


class MenuCalibrationFrame(AppFrame):
    def __init__(self, app, parent, row, column, rowspan, columnspan, sticky):
        AppFrame.__init__(self, app, parent, row, column, rowspan, columnspan, sticky)

        self.actions = MenuCalibrationActions(self.app, self.frame, 0, 0, 1, 1, (S, N,E,W))
        self.list = MenuCalibrationList(self.app, self.frame, 1, 1, 1, 1, (S,N,E,W))


    def create_button(self, button_id, title, callback, padx = 0, pady = 0, Show=False):
        self.actions.buttons[button_id] = {
            'node': Button(self.actions.frame, text=title, command=callback),
            'padx': padx,
            'pady': pady
        }
        if Show: self.actions.buttons[button_id]['node'].pack(padx=padx, pady=pady, fill=X)

    def show(self):
        self.frame.grid(column=self.column, row=self.row, rowspan=self.rowspan, columnspan=self.columnspan, sticky=self.sticky)
        self.actions.show()
        self.list.show()

    def hide(self):
        self.frame.grid_forget()
        self.actions.hide()
        self.list.hide()

    def get_questions(self):
        qs = self.list.questions
        result = {}
        for q in qs:
            cur_q = qs[q]
            result[cur_q.question_name.get()] = {
                "coord": cur_q.coord,
                "criterias": ",".join(cur_q.criterias)
            }
        return result

    def disable_button(self, button_id):
        self.actions.buttons[button_id]['node'].config(state = DISABLED)

    def enable_button(self, button_id):
        self.actions.buttons[button_id]['node'].config(state = NORMAL)

    def start_region_capture(self):
        self.actions.start_region_capture()

    def end_region_capture(self, region):
        self.actions.end_region_capture()
        self.list.end_region_capture(region)

    def start_paper_crop(self):
        self.actions.start_paper_crop()

    def end_paper_crop(self):
        self.actions.end_paper_crop()
