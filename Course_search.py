from tkinter import *
from Course_Search_lib import InvalidCourse, InvalidLevel, InvalidInstructor, CourseList, Course, Online, InPerson, main

# Load courses by calling the main function from the class file
main()

class MyFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.data = StringVar()
        self.create_components()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_components(self):
        self.clear_frame()

        # Welcome label
        welcome_label = Label(self, text="Welcome to the Course Repository")
        welcome_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Search buttons
        title_button = Button(self, text="Search By Title", command=self.title_btn_click)
        instructor_button = Button(self, text="Search By Instructor", command=self.instructor_btn_click)
        level_button = Button(self, text="Search By Course Level", command=self.level_btn_click)

        # Layout buttons
        title_button.grid(row=1, column=0, columnspan=2, pady=5)
        instructor_button.grid(row=2, column=0, columnspan=2, pady=5)
        level_button.grid(row=3, column=0, columnspan=2, pady=5)

    def title_btn_click(self):
        self.clear_frame()

        # Title input
        title_label = Label(self, text="Enter Title:")
        title_label.grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = Entry(self)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Next and Main Menu buttons
        next_button = Button(self, text="Next", command=self.title_next_handler)
        next_button.grid(row=1, column=0, pady=5)
        main_menu_button = Button(self, text="Main Menu", command=self.create_components)
        main_menu_button.grid(row=1, column=1, pady=5)

        # Results display
        results_label = Label(self, text="Search results appear below:")
        results_label.grid(row=2, column=0, columnspan=2, pady=5)
        self.data.set('')
        course_info_label = Label(self, textvariable=self.data, justify=LEFT)
        course_info_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def instructor_btn_click(self):
        self.clear_frame()

        # Instructor input
        instructor_label = Label(self, text="Enter Instructor Name:")
        instructor_label.grid(row=0, column=0, padx=5, pady=5)
        self.instructor_entry = Entry(self)
        self.instructor_entry.grid(row=0, column=1, padx=5, pady=5)

        # Next and Main Menu buttons
        next_button = Button(self, text="Next", command=self.instructor_next_handler)
        next_button.grid(row=1, column=0, pady=5)
        main_menu_button = Button(self, text="Main Menu", command=self.create_components)
        main_menu_button.grid(row=1, column=1, pady=5)

        # Results display
        results_label = Label(self, text="Search results appear below:")
        results_label.grid(row=2, column=0, columnspan=2, pady=5)
        self.data.set('')
        course_info_label = Label(self, textvariable=self.data, justify=LEFT)
        course_info_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def level_btn_click(self):
        self.clear_frame()

        # Level input
        level_label = Label(self, text="Enter Course Level (UG/G):")
        level_label.grid(row=0, column=0, padx=5, pady=5)
        self.level_entry = Entry(self)
        self.level_entry.grid(row=0, column=1, padx=5, pady=5)

        # Next and Main Menu buttons
        next_button = Button(self, text="Next", command=self.level_next_handler)
        next_button.grid(row=1, column=0, pady=5)
        main_menu_button = Button(self, text="Main Menu", command=self.create_components)
        main_menu_button.grid(row=1, column=1, pady=5)

        # Results display
        results_label = Label(self, text="Search results appear below:")
        results_label.grid(row=2, column=0, columnspan=2, pady=5)
        self.data.set('')
        course_info_label = Label(self, textvariable=self.data, justify=LEFT)
        course_info_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def title_next_handler(self):
        key = self.title_entry.get()
        search_criteria = 't'
        try:
            matching_courses = Course.all_courses.search(key, search_criteria)
            if matching_courses:
                result = ''
                for course in matching_courses:
                    result += str(course) + '\n'
                self.data.set(result)
            else:
                raise InvalidCourse()
        except InvalidCourse as e:
            self.data.set(str(e))

    def instructor_next_handler(self):
        key = self.instructor_entry.get()
        search_criteria = 'i'
        try:
            matching_courses = Course.all_courses.search(key, search_criteria)
            if matching_courses:
                result = ''
                for course in matching_courses:
                    result += str(course) + '\n'
                self.data.set(result)
            else:
                raise InvalidInstructor()
        except InvalidInstructor as e:
            self.data.set(str(e))

    def level_next_handler(self):
        key = self.level_entry.get()
        search_criteria = 'l'
        try:
            matching_courses = Course.all_courses.search(key, search_criteria)
            if matching_courses:
                result = ''
                for course in matching_courses:
                    result += str(course) + '\n'
                self.data.set(result)
            else:
                raise InvalidLevel()
        except InvalidLevel as e:
            self.data.set(str(e))

root = Tk()
root.title("Course Options")
root.geometry("400x400")

app = MyFrame(root)
app.grid()

root.mainloop()
