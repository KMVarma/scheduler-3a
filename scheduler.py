import readcsv
import planner
import pdb

# Creates course dict and prints first 5 entries
course_dict = readcsv.create_course_dict()


def course_scheduler (course_descriptions, goal_conditions, initial_state):
    # any prior credits are added to classes taken
    classes_taken = set()
    for course in initial_state:
        classes_taken.add(course)
    schedule = []
    plan = satisfy_goals(goal_conditions, classes_taken, schedule)
    print(plan)
    return plan

def satisfy_goals(goal_conditions, taken, schedule):

    if not goal_conditions:    # base case, no goals left to satisfy
        return schedule

    while goal_conditions:
        # iteratively satisfy all goal conditions
        goal = goal_conditions[0]
        prereqs = get_prereqs(goal)

        classes_to_satisfy = []
        for option in prereqs:
            classes_to_satisfy.append([x for x in option if x not in taken])

        if not classes_to_satisfy:  # no prereqs
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
                    # if [] is in classes_to_satisfy, then the prereqs have already been satisfied and any other option
                    # can be ignored
                    # todo: maybe figure out a way to pick the easiest option first rather than the first option?
                    if not [] in classes_to_satisfy:
                        option = classes_to_satisfy[i]
                    if satisfy_goals(option, taken, schedule):
                        info = get_course_info(goal)
                        if info.credits != '0':
                            taken.add(goal)
                            schedule.append((goal, prereqs[i]))
                        if goal_conditions:
                            goal_conditions.pop(0)
                        unsatisfied = False
                    else:
                        # the option could not be satisfied
                        i += 1
                else:
                    # no option left to satisfy the goal's prereqs
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
    # check if have already taken\n",
    for potential_courses in course_info.prereqs:
        needed_courses = [course for course in potential_courses]
        prereqs.append(needed_courses)
    return prereqs

# Helper function for get_prereqs\n",
# Given a readcsv.Course returns its corresponding readcsv.CourseInfo\n",
def get_course_info(target_course):
    for course, course_info in course_dict.items():
        if target_course[0] == course.program and target_course[1] == course.designation:
            return course_info
    raise ValueError('Course: {} not found in course catalog'.format(target_course))
    return 'ERROR'


course_scheduler(course_dict, [('CS', 'calculus')], [])
