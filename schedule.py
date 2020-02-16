from semester import Semester
import random


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
        self.MAX_HOURS = 18
        self.MIN_HOURS = 12
        self.course_dict = course_dict
        self.taken = []

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
            course_to_move = targetsem.courses[1]
            targetsem.remove(course_to_move)
            self.add_course(course_to_move, semester_idx + 1)
        self.schedule[semester_idx].add(course)
        self.taken.append(course)
        return True

    def get_rand_no_prereqs(self):
        no_prereq_classes = []
        for course_name, course in self.course_dict.items():
            if len(sum(course.prereqs, [])) == 0:
                no_prereq_classes.append(course)

        return no_prereq_classes

    def fill_to_min(self):
        no_prereqs = self.get_rand_no_prereqs()
        for semester in self.schedule:
            while semester.hours < self.MIN_HOURS:
                choice = random.choice(no_prereqs)
                if choice in self.taken:
                    no_prereqs.remove(choice)
                else:
                    semester.add(choice)
                    no_prereqs.remove(choice)


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
            result = self.add_course(course, 0)
            if not result:
                return False
        self.fill_to_min()
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

    def format_plan(self):
        # ((“CS”, “2201”), (“Spring”, “Frosh”), 3)
        plan = []
        for i in range(8):
            if self.schedule[i].courses:
                for course in self.schedule[i].courses:
                    plan.append((course, self.schedule[i].date, course.hours))
        return tuple(plan)