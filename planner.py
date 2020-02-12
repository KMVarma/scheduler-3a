

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
        self.MAX_HOURS = 18
        self.MIN_HOURS = 12

    def add_course(self, course, semester_idx):
        '''
        expects course object
        searches for earlies appropriate semester to add course
        '''

        # check for course conflicts
        conflicting_courses = []
        moved_hours = 0
        for scheduled_course in self.schedule[semester_idx].courses:
            if course.name in scheduled_course.prereqs:
                conflicting_courses.append(scheduled_course)
                moved_hours += scheduled_course.hours

        # conditions for throwing errors
        if (len(conflicting_courses) > 0) and semester_idx > 6:
            print('Scheduling not possible')
            exit(-1)

        # reschedule any course conflicts
        for scheduled_course in conflicting_courses:
            self.schedule[semester_idx].remove(scheduled_course)
            self.add_course(scheduled_course, semester_idx + 1)

        # shift chain of courses up if not enough hours in semester to fit
        if self.schedule[semester_idx].hours - moved_hours + course.hours > self.MAX_HOURS:
            if semester_idx > 6:
                print('Scheduling not possible')
                exit(-1)
            self.add_course(course, semester_idx + 1)
        else:
            self.schedule[semester_idx].add(course)

    def remove_course(self, course, semester):
        '''
        expects int semester
        '''
        self.schedule[semester].remove(course)

    def find_hours(self, course):
        return int(self.course_dict[course].credits)

    def __str__(self):
        string = ''
        for sem in self.schedule:
            string += str(sem)
        return string

    def clear(self):
        for sem in self.schedule:
            sem.clear()

    def planner(self, semesterlist):
        for name, prereqs in reversed(semesterlist):
            course = Course(name, prereqs, self.find_hours(name))
            print(course)
            self.add_course(course, 0)

    def is_good(self):
        for semester in self.schedule:
            hours = semester.hours
            if hours > 18:
                return False
            if hours < 12 and not semester.date == ('Spring', 'Senior'):
                return False
        return True


class Course:
    def __init__(self, name, prereqs, hours):
        self.name = name
        self.prereqs = prereqs
        self.hours = hours

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()
