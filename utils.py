import readcsv

course_dict = readcsv.create_course_dict()


def get_course_info(target_course):
    for course, course_info in course_dict.items():
        if target_course[0] == course.program and target_course[1] == course.designation:
            return course_info
    raise ValueError('Course: {} not found in course catalog'.format(target_course))

# if it was empty, note that index and take it from prereqs

# Given a course returns all possible ways to satisfy the requirements.
# params:
#    course - readcsv.Course object, course name (key in course_dict)
#    taken_classes - set of readcsv.Course objects of classes that have already been taken
# returns:
#    list of lists, each list has readcsv.Course objects of classes to fufill the requirement
#    ie. CSliberalhum would return [[('HIST', '2700'), ('ENGL', '3896')], [('ENGL', '1250W'), ('EUS', '2203')]]
#    since the liberal humanities req can be satisfied by either two class set.
def get_prereqs(course):
    prereqs = []
    course_info = get_course_info(course)
    if not course_info:
      return prereqs
    return format_prereqs(course_info.prereqs)


def format_prereqs(prereqs_tuple):
    prereqs = []
    for potential_courses in prereqs_tuple:
        needed_courses = [course for course in potential_courses]
        prereqs.append(needed_courses)
    return prereqs