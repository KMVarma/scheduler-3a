from schedule import Schedule
from utils import course_dict, get_course_info, get_prereqs
import time

def course_scheduler (course_descriptions, goal_conditions, initial_state, course_macros):
    """
    returns a list of courses (with their respective prereqs) that need to be satisfied to satisfy the goal conditions

    :param course_descriptions: course dictionary
    :param goal_conditions: goals that need to be satisfied
    :param initial_state: courses that have already been taken
    :param course_macros: dictionary of high-level requirements and sequence of classes to satisfy
    :return: a list of course-prereq tuples [(course1, [prereqs]), (course2, [prereqs]), ...] that need to be scheduled
    """
    # any prior credits are added to classes taken
    classes_taken = set()
    for course in initial_state:
        classes_taken.add(course)
    schedule = []
    plan = satisfy_goals(goal_conditions, classes_taken, schedule, course_macros)
    # print(plan)
    return plan

def satisfy_goals(goal_conditions, taken, schedule, course_macros):
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

    while goal_conditions:
        # iteratively satisfy all goal conditions
        goal = goal_conditions[0]

        using_macro = False
        # if goal is in macros use precomputed courses
        for macro, prereqs in course_macros.items():
            if macro == goal:
                using_macro = True
                for course in prereqs:
                    if course[0] not in taken:
                        taken.add(course[0])
                        schedule.append(course)
                goal_conditions.pop(0)
        if using_macro:
            continue

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
                    if satisfy_goals(option, taken, schedule, course_macros):
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


# Given a high level goal creates a dict of immediate subgoals and a way to satisfy them
def create_macros(course_descriptions, goal_condition):
    goals = get_prereqs(goal_condition)[0]
    macros_dict = {}
    for goal in goals:
        macros_dict[goal] = course_scheduler(course_descriptions, [goal], [], {})

    return macros_dict

if __name__ == '__main__':

    macros_dict = create_macros(course_dict, ('CS', 'major'))
    start_time = time.clock()
    courselist = course_scheduler(course_dict, [('CS', 'major')], [], macros_dict)

    duration = time.clock() - start_time
    schedule = Schedule()
    schedule.planner(courselist)
    print("Schedule found in ", duration, " seconds.")
    print(schedule)