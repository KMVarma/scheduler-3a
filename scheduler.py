from schedule import Schedule
import readcsv
from utils import format_prereqs
from course import Course
import time

course_dict = readcsv.create_course_dict()
new_dict = {}
for course, course_info in course_dict.items():
    new_dict[(course.program, course.designation)] = \
        Course((course.program, course.designation),
               format_prereqs(course_info.prereqs), course_info.terms, int(course_info.credits))
course_dict = new_dict

def course_scheduler (goal_conditions, initial_state, course_macros, goal_name):
    """
    returns a list of courses (with their respective prereqs) that need to be satisfied to satisfy the goal conditions

    :param goal_conditions: goals that need to be satisfied
    :param initial_state: courses that have already been taken
    :param course_macros: dictionary of high-level requirements and sequence of classes to satisfy
    :return: a list of course-prereq tuples [(course1, [prereqs]), (course2, [prereqs]), ...] that need to be scheduled
    """
    # any prior credits are added to classes taken
    classes_taken = []
    for course in initial_state:
        classes_taken.append(course)
    schedule = []
    plan = satisfy_goals(goal_conditions, classes_taken, schedule, course_macros, goal_name)
    # print(plan)
    return plan

def satisfy_goals(goal_conditions, taken, schedule, course_macros, goal_name = ''):
    """
    satisfies goal conditions by recursively breaking each goal into prereqs

    :param goal_conditions: goals that need to be satisfied
    :param taken: courses that have already been taken
    :param schedule: a list of course-prereq tuples [(course1, [prereqs]), (course2, [prereqs]), ...]
    that need to be scheduled
    :param course_macros: dictionary of high-level requirements and sequence of classes to satisfy
    :return: a schedule
    """
    if not goal_conditions:    # base case, no goals left to satisfy
        return schedule
    if goal_name == ('CS', 'open2'):
        print('here')
    while goal_conditions:
        # iteratively satisfy all goal conditions
        goal = goal_conditions[0]

        using_macro = False
        # if goal is in macros use precomputed courses
        for macro, prereqs in course_macros.items():
            if macro == goal:
                for course in prereqs:
                    if course not in taken:
                        using_macro = True
                        taken.append(course)
                        schedule.append(course)
                goal_conditions.pop(0)
        if using_macro:
            continue

        # keeping track of the prereqs that were required (in prereqs) and the prereqs that are actually needed
        # (in classes_to_satisfy)
        # prereqs = get_prereqs(goal)
        #prereqs2 =prereqs
        classes_to_satisfy = []
        # for option in prereqs:
        for option in goal.prereqs:
            # classes_to_satisfy.append([x for x in option if x not in taken])
            classes_to_satisfy.append([course_dict[x] for x in option])

        if not classes_to_satisfy:  # no prereqs needed
            # info = get_course_info(goal)
            if goal == ('BASS', '1000'):
                print('here')
            # if goal in taken:
                # print('duplicate')
                # return ()
            # if info.credits != '0' and goal not in taken:    # if credits is '0', it's a high-level requirement (not an actual course)
            #     # Create course to be added
            #     course = Course.from_name(goal)
            #     taken.append(course)
            #     course.satisfies.append(goal_name)
            #     schedule.append(course)
            if goal.hours != 0 and goal not in taken:    # if credits is '0', it's a high-level requirement (not an actual course)
                # Create course to be added
                taken.append(goal)
                goal.satisfies.append(goal_name)
                schedule.append(goal)
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
                    if option == ('BASS', '1000') or ('BASS', '1000') in option:
                        print('here')
                        test = option
                        result = option[0] in test
                        if test in taken:
                            print(True)
                    if satisfy_goals(option, taken, schedule, course_macros, goal):
                        if goal_name == str(('CS', 'open1')):
                            print('here')
                        # info = get_course_info(goal)
                        # if info.credits != '0' and goal not in taken:
                        #     # Create course to be added
                        #     course = Course.from_name(goal)
                        #     taken.append(course)
                        #     course.satisfies.append(goal_name)
                        #     schedule.append(course)
                        if goal.hours != 0 and goal not in taken:  # if credits is '0', it's a high-level requirement (not an actual course)
                            # Create course to be added
                            taken.append(goal)
                            goal.satisfies.append(goal_name)
                            schedule.append(goal)
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


# Given a high level goal creates a dict of immediate subgoals and a way to satisfy them
def create_macros(goal_condition):
    macros_dict = {}
    for goal in goal_condition.prereqs:
        # goal = Course.from_name(name)
        macros_dict[goal] = course_scheduler([goal], [], {}, str(goal_condition))

    return macros_dict

if __name__ == '__main__':
    # target = Course.from_name(('CS', 'major'))
    target = course_dict['CS', 'major']
    imports = []

    macros_dict = {}
    # macros_dict = create_macros(target)
    # for macro, prereqs in macros_dict.items():
    #     for prereq in prereqs:
    #         prereq.satisfies.append(macro)
    start_time = time.time()
    courselist = course_scheduler([target], imports, macros_dict, str(('CS', 'major')))
    # courselist = [Course.from_name(name) for name, _ in courselist]
    schedule = Schedule()
    schedule.planner(courselist)
    duration = time.time() - start_time

    print("Schedule found in {:4f} seconds.".format(duration))
    print(schedule)