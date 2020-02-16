from schedule import Schedule
import readcsv
from utils import format_prereqs
from course import Course
import time



def course_scheduler (course_descriptions, goal_conditions, initial_state):
    """
    returns a list of courses (with their respective prereqs) that need to be satisfied to satisfy the goal conditions

    :param goal_conditions: goals that need to be satisfied
    :param initial_state: courses that have already been taken
    :param course_macros: dictionary of high-level requirements and sequence of classes to satisfy
    :return: a list of course-prereq tuples [(course1, [prereqs]), (course2, [prereqs]), ...] that need to be scheduled
    """
    course_dict = reformat_dict(course_descriptions)
    start_time = time.time()
    cpu_time = time.clock()
    goals = []
    for goal in goal_conditions:
        goals.append(course_dict[goal])
    # any prior credits are added to classes taken
    classes_taken = []
    for init in initial_state:
        classes_taken.append(course_dict[init])
    schedule = []
    course_macros = create_macros(course_dict, goal_conditions)
    goal_name = course_dict['CS', 'major']

    courselist = satisfy_goals(course_dict, goals, classes_taken, schedule, course_macros, goal_name)

    planner = Schedule()
    result = planner.planner(courselist)

    if not result:
        return ()

    duration = time.time() - start_time
    cpu_duration =  time.clock() - cpu_time
    print("Schedule found in {:4f} wall seconds.".format(duration))
    print("Schedule found in {:4f} cpu seconds.".format(cpu_duration))
    print(planner)
    return planner.format_plan()

def reformat_dict(course_dict):
    new_dict = {}
    for course, course_info in course_dict.items():
        new_dict[(course.program, course.designation)] = \
            Course((course.program, course.designation),
                   format_prereqs(course_info.prereqs), course_info.terms, int(course_info.credits))
    return new_dict

def satisfy_goals(course_dict, goal_conditions, taken, schedule, course_macros, goal_name):
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
        classes_to_satisfy = []
        # for option in prereqs:
        for option in goal.prereqs:
            classes_to_satisfy.append([course_dict[x] for x in option])

        if not classes_to_satisfy:  # no prereqs needed
            # info = get_course_info(goal)
            goal_prefix = goal_name.name[0]
            search_space = goal.satisfies
            result = False
            for course in search_space:
                if goal_prefix == course.name[0] and goal_name.hours == 0:
                    result = True
                    break
            if result:
                return False

            planner = Schedule()
            result = planner.planner(schedule)

            if not result:
                return False
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
                    result = False
                    for o in option:
                        # if o in taken:
                        #     break
                        goal_prefix = goal.name[0]
                        search_space = o.satisfies
                        result = False
                        for course in search_space:
                            if goal_prefix == course.name[0] and goal.hours == 0 and goal.name[1] != course.name[1]:
                                result = True
                                i += 1
                                break
                    if result:
                        continue
                    if satisfy_goals(course_dict, option, taken, schedule, course_macros, goal):
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
                    return []
    return schedule


# Given a high level goal creates a dict of immediate subgoals and a way to satisfy them
def create_macros(course_dict, goal_condition):
    macros_dict = {}
    for name in goal_condition:
        goal = course_dict[name]
        for prereq in sum(goal.prereqs, []):
            schedule = []
            plan = satisfy_goals(course_dict, [course_dict[prereq]], [], schedule, {}, Course(('Main', 'Main'), [], [], 0))
            # print(plan)
            macros_dict[prereq] =  plan

    return macros_dict

if __name__ == '__main__':
    course_descriptions = readcsv.create_course_dict()
    planner = course_scheduler(course_descriptions, [('CS', 'major')], [])
