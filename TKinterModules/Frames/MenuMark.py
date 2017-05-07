from Tkinter import *
from ..AppFrame import AppFrame

class MenuMarkFrame(AppFrame):
    def __init__(self, app, parent, row, column, rowspan, columnspan, sticky):
        AppFrame.__init__(self, app, parent, row, column, rowspan, columnspan, sticky)
        Label(self.frame, text="Mark Menu").pack(padx=5, pady=5, fill=X)
        self.criterias = []

    def init_mark_paper(self, questions):
        self.questions = questions

        self.current_page = 1
        self.page_count = len(questions)

        for question in self.questions:
            criteria_widgets = []

            criterias = question["criterias"]
            for criteria in criterias:
                criteria = criteria.split(":")
                val = IntVar()
                criteria_widgets.append({
                    "weight": criteria[1],
                    "name": criteria[0],
                    "val": val,
                    "checker": Checkbutton(self.frame, text=criteria[0] + " - " + criteria[1], variable=val)
                })
            self.criterias.append(criteria_widgets)
        self.__load_question_criteria(self.current_page - 1)
        
    def next_page(self):
        cur_page = int(self.current_page)
        max_page = int(self.page_count)
        if cur_page < max_page:
            self.__unload_question_criteria(self.current_page - 1)
            self.current_page += 1
            self.__load_question_criteria(self.current_page - 1)

    def prev_page(self):
        cur_page = int(self.current_page)
        max_page = int(self.page_count)
        if cur_page > 1:
            self.__unload_question_criteria(self.current_page - 1)
            self.current_page -= 1
            self.__load_question_criteria(self.current_page - 1)

    def __unload_question_criteria(self, index):
        cur_question = self.criterias[index]
        for widget in cur_question:
            widget["checker"].pack_forget()

    def __load_question_criteria(self, index):
        cur_question = self.criterias[index]
        for widget in cur_question:
            widget["checker"].pack(padx=5, pady=5, fill=X)
