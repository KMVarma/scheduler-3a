from utils import get_course_info
from semester import Semester
from course import Course


class Schedule:
    def __init__(self):
        self.schedule = [Semester('Fall', 'Frosh'),
                         Semester('Spring', 'Frosh'),
                         Semester('Fall', 'Soph'),
                         Semester('Spring', 'Soph'),
                         Semester('Fall', 'Junior'),
                         Semester('Spring', 'Junior'),
                         Semester('Fall', 'Senior'),
                         Semester('Spring', 'Senior')]
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
            info = get_course_info(name)
            course = Course(name, sum(prereqs, []), info.terms, int(info.credits))
            self.add_course(course, 0)

    def is_good(self):
        for semester in self.schedule:
            hours = semester.hours
            if hours > 18:
                return False
            if hours < 12 and not semester.date == ('Spring', 'Senior'):
                return False
        return True

    def total_hours(self):
        sum = 0
        for semester in self.schedule:
            sum += semester.hours
        return sum