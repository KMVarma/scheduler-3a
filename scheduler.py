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
    prereqs = set()
    plan = satisfy_goals(goal_conditions, classes_taken, schedule, prereqs)
    print(plan)
    return plan

def satisfy_goals(goal_conditions, taken, schedule, prereqs):

    if not goal_conditions:    # base case, no goals left to satisfy
        return schedule

    while goal_conditions:
        # iteratively satisfy all goal conditions
        goal = goal_conditions[0]
        classes_to_satisfy = get_prereqs(goal, taken)

        if not classes_to_satisfy:  # no prereqs
            info1 = get_course_info(goal)
            if info1.credits != '0':    # if credits is '0', it's a high-level requirement (not an actual course)
                taken.add(goal)
                schedule.append((goal, prereqs))
                print('added')
            goal_conditions.pop(0)

        else:   # there are prereqs
            unsatisfied = True
            while unsatisfied:
                if classes_to_satisfy:
                    option = []
                    # if [] is in classes_to_satisfy, then the prereqs have already been satisfied and any other option
                    # can be ignored
                    # todo: maybe figure out a way to pick the easiest option first rather than the first option?
                    if not [] in classes_to_satisfy:
                        option = classes_to_satisfy[0]
                        for option1 in option:
                            prereqs.add(option1)
                    if satisfy_goals(option, taken, schedule, set()):
                        info1 = get_course_info(goal)
                        if info1.credits != '0':
                            taken.add(goal)
                            schedule.append((goal, prereqs))
                        goal_conditions.pop(0)
                        unsatisfied = False
                    else:
                        # the option could not be satisfied
                        classes_to_satisfy.remove(option)
                        for option1 in option:
                            prereqs.remove(option1)
                else:
                    # no option left to satisfy the goal's prereqs
                    return ()
    return schedule

# Given a course returns all possible ways to satisfy the requirements.
# params:
#    course - readcsv.Course object, course name (key in course_dict)
#    taken_classes - set of readcsv.Course objects of classes that have already been taken
# returns:
#    list of lists, each list has readcsv.Course objects of classes to fufill the requirement
#    ie. CSliberalhum would return [[('HIST', '2700'), ('ENGL', '3896')], [('ENGL', '1250W'), ('EUS', '2203')]]
#    since the liberal humanities req can be satisfied by either two class set.
def get_prereqs(course, taken_classes):
  prereqs = []
  #print('Course to get prereq for: ', course)
  course_info = get_course_info(course)
  #print('Get course info returns: ', course_info)
  if not course_info:
    return prereqs
  # check if have already taken
  for potential_courses in course_info.prereqs:
    needed_courses = [ course for course in potential_courses if course not in taken_classes ]
    prereqs.append(needed_courses)

  return prereqs

# Helper function for get_prereqs
# Given a readcsv.Course returns its corresponding readcsv.CourseInfo
def get_course_info(target_course):
  for course, course_info in course_dict.items():
    if target_course[0] == course.program and target_course[1] == course.designation:
      return course_info
  raise ValueError('Course: {} not found in course catalog'.format(target_course))
  return 'ERROR'

def print_schedule(schedule):
    for sem in schedule.schedule:
        print(sem.date, sem.courses)

course_scheduler(course_dict, [('CS', 'calculus')], [])