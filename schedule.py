from semester import Semester


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
        if semester_idx > 7:
            # raise ValueError('Can\'t fit course')
            return False
        targetsem = self.schedule[semester_idx]
        if targetsem.date[0] not in course.terms:
            return self.add_course(course, semester_idx + 1)

        # check for course conflicts
        conflicting_courses = []
        moved_hours = 0
        for scheduled_course in targetsem.courses:
            if course.name in sum(scheduled_course.prereqs, []):
                conflicting_courses.append(scheduled_course)
                moved_hours += scheduled_course.hours

        # conditions for throwing errors
        if (len(conflicting_courses) > 0) and semester_idx > 6:
            # raise ValueError('Can\'t fit course')
            return False

        # reschedule any course conflicts
        for scheduled_course in conflicting_courses:
            targetsem.remove(scheduled_course)
            self.add_course(scheduled_course, semester_idx + 1)

        # shift chain of courses up if not enough hours in semester to fit
        while targetsem.hours + course.hours > self.MAX_HOURS:
            if semester_idx > 6:
                # raise ValueError('Can\'t fit course')
                return False

            #choose a random course (last one since it most likely has the least dependencies)
            course_to_move = targetsem.courses[-1]
            targetsem.remove(course_to_move)
            self.add_course(course_to_move, semester_idx + 1)
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
        string += 'Total Hours: ' + str(self.total_hours())
        return string

    def clear(self):
        for sem in self.schedule:
            sem.clear()

    def planner(self, course_list):
        for course in reversed(course_list):
            self.add_course(course, 0)
        return True

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