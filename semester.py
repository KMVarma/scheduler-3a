class Semester:
    def __init__(self, semester, year):
        self.courses = []
        self.date = (semester, year)
        self.hours = 0

    def add(self, course):
        '''
        course: course to add
        hours: int hours that course is worth
        '''
        self.courses += [course]
        self.hours += course.hours

    def remove(self, course):
        '''
        course: course to remove
        hours: int hours that course is worth
        '''
        self.courses.remove(course)
        self.hours -= course.hours

    def clear(self):
        self.courses = []
        self.hours = 0

    def __str__(self):
        return '******************************************************\n' \
               + str(self.date) + '\n' \
               + 'Courses' + str(self.courses) + '\n' \
               + 'Hours: ' + str(self.hours) + '\n'
