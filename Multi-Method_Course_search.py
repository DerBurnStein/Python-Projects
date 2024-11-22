# -------------------------------------------------------------------------------
# HA3
# Student Name: Jeremy Southern
# Python version: 3.9
# -------------------------------------------------------------------------------

class InvalidCourse(Exception):
    def __str__(self):
        return 'Course not found!'


class InvalidInstructor(Exception):
    def __str__(self):
        return 'Invalid instructor'


class InvalidLevel(Exception):
    def __str__(self):
        return 'Invalid level'


class InvalidOption(Exception):
    def __str__(self):
        return 'Invalid Option'


class CourseList(list):
    def search(self, key, search_criteria):
        matching_courses = []
        if search_criteria == 't':
            for course in self:
                if course.title == key:
                    matching_courses.append(course)
        elif search_criteria == 'i':
            for course in self:
                if course.instructor == key:
                    matching_courses.append(course)
        elif search_criteria == 'l':
            for course in self:
                if course.level == key:
                    matching_courses.append(course)
        else:
            raise InvalidOption()
        if not matching_courses:
            raise InvalidCourse()
        return matching_courses


class Course(object):
    all_courses = CourseList()

    def __init__(self, level, course_id, title, instructor):
        self.level = level
        self.course_id = course_id
        self.title = title
        self.instructor = instructor
        Course.all_courses.append(self)

    def __str__(self):
        return f"Level#: {self.level}\nID: {self.course_id}\nTitle: {self.title}\nInstructor: {self.instructor}"


class InPerson(Course):
    def __init__(self, level, course_id, title, instructor, campus, location, capacity):
        super().__init__(level, course_id, title, instructor)
        self.campus = campus
        self.location = location
        self.capacity = capacity

    def __str__(self):
        return super().__str__() + f"Campus: {self.campus}\n Location: {self.location}\nCapacity: {self.capacity}"


class Online(Course):
    def __init__(self, level, course_id, title, instructor):
        super().__init__(level, course_id, title, instructor)
        self.location = 'Online'

    def __str__(self):
        return super().__str__() + f"Location: {self.location}"


def main():
    print("--------------------------------")
    print("Welcome to course database main menu:")
    print("--------------------------------")

    courses_list = CourseList()
    with open('courses.txt', 'r') as courses:
        for line in courses:
            line = line.split(',')
            if line[-1] == 'Online\n':
                course = Online(line[0], line[1], line[2], line[3])
            elif len(line) == 7:
                course = InPerson(line[0], line[1], line[2], line[3], line[4], line[5], line[6])
            courses_list.append(course)

    choice = ''
    menu = "\nSearch by course title[t]\nSearch by Instructor[i]\nSearch by Level[l]\nExit[e]:"

    while choice != 'e':
        print(menu)
        choice = input("Enter choice (t/i/l/e): ")
        try:
            if choice == 't':
                key = input("Enter course title: ")
                search_list = courses_list.search(key, 't')
            elif choice == 'i':
                key = input("Enter the instructor’s name: ")
                search_list = courses_list.search(key, 'i')
            elif choice == 'l':
                key = input("Enter the level (UG/G): ")
                search_list = courses_list.search(key, 'l')
            elif choice == 'e':
                print('Exiting the database...')
                break
            else:
                raise InvalidOption()
            for course in search_list:
                print(course)

        except InvalidOption:
            print("Invalid Option. Returning to main...")
        except InvalidCourse:
            print("Course not found!")
        except InvalidLevel:
            print("Course level not found!")
        except InvalidInstructor:
            print("Instructor not found!")


main()
