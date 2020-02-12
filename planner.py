

class Semester:
    def __init__(self, semester, year):
        self.courses = []
        self.date = (semester, year)
        self.hours = 0

    def add(self, course, hours):
        '''
        course: course to add
        hours: int hours that course is worth
        '''
        self.courses += [course]
        self.hours += hours

    def remove(self, course, hours):
        '''
        course: course to remove
        hours: int hours that course is worth
        '''
        self.courses.remove(course)
        self.hours -= hours

    def clear(self):
        self.courses = []
        self.hours = 0

    def __str__(self):
        return '******************************************************\n' \
               + str(self.date) + '\n' \
               + 'Courses' + str(self.courses) + '\n' \
               + 'Hours: ' + str(self.hours) + '\n'


class Schedule:
    def __init__(self, course_dict):
        self.schedule = [Semester('Fall', 'Frosh'),
                         Semester('Spring', 'Frosh'),
                         Semester('Fall', 'Soph'),
                         Semester('Spring', 'Soph'),
                         Semester('Fall', 'Junior'),
                         Semester('Spring', 'Junior'),
                         Semester('Fall', 'Senior'),
                         Semester('Spring', 'Senior')]
        """
        self.schedule = [Semester('Spring', 'Senior'),
                         Semester('Fall', 'Senior'),
                         Semester('Spring', 'Junior'),
                         Semester('Fall', 'Junior'),
                         Semester('Spring', 'Soph'),
                         Semester('Fall', 'Soph'),
                         Semester('Spring', 'Frosh'),
                         Semester('Fall', 'Frosh'),
                         ]
        """
        self.course_dict = course_dict

    def add_course(self, course, semester):
        '''
        expects int semester
        '''
        self.schedule[semester].add(course, self.find_hours(course))

    def remove_course(self, course, semester):
        '''
        expects int semester
        '''
        self.schedule[semester].remove(course, self.find_hours(course))

    def find_hours(self, course):
        return int(self.course_dict[course].credits)

    def move_course(self, course, prev, future):
        self.remove_course(course, prev)
        self.add_course(course, future)

    def __str__(self):
        string = ''
        for sem in self.schedule:
            string += str(sem)
        return string

    def clear(self):
        for sem in self.schedule:
            sem.clear()

    def planner(self, semesterlist):
        '''
        List of list of classes that need to be added, each internal list representing a semester
        Strategy is to add classes as early as possible and push them back only when necessary
        Assumes that class prereqs have already been determined
        '''
        current_sem = 0
        for semester in semesterlist:
            for course in semester:
                self.add_course(course, current_sem)
            current_sem += 1


