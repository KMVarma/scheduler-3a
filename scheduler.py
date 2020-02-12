import readcsv
import planner
import pdb

# Creates course dict and prints first 5 entries
course_dict = readcsv.create_course_dict()


def course_scheduler (course_descriptions, goal_conditions, initial_state):
    """
    returns a list of courses (with their respective prereqs) that need to be satisfied to satisfy the goal conditions

    :param course_descriptions: course dictionary
    :param goal_conditions: goals that need to be satisfied
    :param initial_state: courses that have already been taken
    :return: a list of course-prereq tuples [(course1, [prereqs]), (course2, [prereqs]), ...] that need to be scheduled
    """
    # any prior credits are added to classes taken
    classes_taken = set()
    for course in initial_state:
        classes_taken.add(course)
    schedule = []
    plan = satisfy_goals(goal_conditions, classes_taken, schedule)
    # print(plan)
    return plan

def satisfy_goals(goal_conditions, taken, schedule):
    """
    satisfies goal conditions by recursively breaking each goal into prereqs

    :param goal_conditions: goals that need to be satisfied
    :param taken: courses that have already been taken
    :param schedule: a list of course-prereq tuples [(course1, [prereqs]), (course2, [prereqs]), ...]
    that need to be scheduled
    :return: a schedule
    """
    if not goal_conditions:    # base case, no goals left to satisfy
        return schedule

    while goal_conditions:
        # iteratively satisfy all goal conditions
        goal = goal_conditions[0]

        # keeping track of the prereqs that were required (in prereqs) and the prereqs that are actually needed
        # (in classes_to_satisfy)
        prereqs = get_prereqs(goal)
        #prereqs2 =prereqs
        classes_to_satisfy = []
        for option in prereqs:
            classes_to_satisfy.append([x for x in option if x not in taken])

        if not classes_to_satisfy:  # no prereqs needed
            info = get_course_info(goal)
            if info.credits != '0':    # if credits is '0', it's a high-level requirement (not an actual course)
                taken.add(goal)
                schedule.append((goal, prereqs))
            goal_conditions.pop(0)

        else:   # there are prereqs
            unsatisfied = True
            noptions = len(classes_to_satisfy)
            i = 0
            while unsatisfied:
                if noptions > i:
                    option = []
                    # if [] is in classes_to_satisfy, then one of the prereq options has already been satisfied and any
                    # other option can be ignored
                    if [] not in classes_to_satisfy:
                        option = classes_to_satisfy[i]  # try the ith prereqs option
                    temp = satisfy_goals(option, taken, schedule)
                    if temp:
                        info = get_course_info(goal)
                        if info.credits != '0':
                            taken.add(goal)
                            schedule.append((goal, prereqs))
                        if goal_conditions:

                            goal_conditions.pop(0)
                        unsatisfied = False
                    else:
                        # the option could not be satisfied
                        i += 1
                else:
                    # no prereq option left to try
                    return ()
    return schedule

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
    for potential_courses in course_info.prereqs:
        needed_courses = [course for course in potential_courses]
        prereqs.append(needed_courses)
    # print('the prereqs of {} are {}'.format(course, prereqs))
    return prereqs

# Helper function for get_prereqs
# Given a readcsv.Course returns its corresponding readcsv.CourseInfo
def get_course_info(target_course):
    for course, course_info in course_dict.items():
        if target_course[0] == course.program and target_course[1] == course.designation:
            return course_info
    raise ValueError('Course: {} not found in course catalog'.format(target_course))
    return 'ERROR'


courselist = course_scheduler(course_dict, [('CS', 'mathematics')], [])
print(courselist)
schedule = planner.Schedule(course_dict)
schedule.planner(courselist)
print(schedule)
pass