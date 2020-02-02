

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
