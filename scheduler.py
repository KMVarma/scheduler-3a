import readcsv
import planner

# Creates course dict and prints first 5 entries
course_dict = readcsv.create_course_dict()
readcsv.print_dict(course_dict, 5)

def course_scheduler (course_descriptions, goal_conditions, initial_state):
    my_schedule = planner.Schedule(course_dict)
    # any prior credits are added to courses taken
    classes_taken = set()
    for course in initial_state:
        classes_taken.add(course)
    
    sem = 0
    # checks whether goal conditions are already met
    if goal_conditions == () or goal_conditions == initial_state:
        return ()

    # iteratively satisfies each goal 
    for goal in goal_conditions:
        goal_reqs = get_prereqs(goal, classes_taken)
        if goal_reqs:
           sem = explore_course(goal_reqs, classes_taken, my_schedule, sem)

        
        classes_taken.add(goal)
        my_schedule.add_course(goal, sem)
    
    
    #   some checks for failure/success somewhere 

    # test to ensure each semester is between 12 and 18 hours
    print(my_schedule)
    return ()

def validity_check(course, prereqs, taken_classes, schedule, sem):

    # check to make sure that courses are not scheduled at the same time as their prereqs
    if ((prereqs == [] or prereqs == [[]]) and schedule.schedule[sem].hours <= 18 and course not in taken_classes ):
        # move to next course
        return True
    else:
        # if there are more prereqs for this course add them to the list of courses to take and push this course up a semester
        return False


#  Given a list of lists performs a depth first search on all the elements of the inner list
#  params:
#     prereqs- a lists of lists containing satisfying prereqs for a course
#     taken_classes- a set of classes that have been taken
#     schedule- a schedule object
#     sem- an integer corresponding to the prospective semester a course will be taken (from 0-7 inclusive)
#
#  returns
#
def explore_course(prereqs, taken_classes, schedule, sem):
    new_sem = 0
    # if you get to the end of this list you've completed one of the goal conditions/satisfying prereq lists for a goal/course
    for outer in prereqs:
        for course in outer:
            if course not in taken_classes:
                schedule.add_course(course, sem)
                new_prereqs = get_prereqs(course, taken_classes)
                
                
                if not validity_check(course, new_prereqs, taken_classes, schedule, sem):
                    
                    new_sem += 1
                    schedule.move_course(course, sem, new_sem)
                    new_sem += explore_course(new_prereqs, taken_classes, schedule, 0)
                taken_classes.add(course)


    return new_sem


# fetch semester of completion for prelims to learn when to schedule a course
# 
def properly_place_course(course, schedule):
    course_info = get_course_info(course)
    prereqs = course_info.prereqs
    sem = 0
    if prereqs:
        for sem_number in schedule.schedule:
            for p in prereqs:
                #check if p is in the schedule
                if p in sem_number:
                    #move on
            sem += 1
    return sem
    return ()

schedule = planner.Schedule(course_dict)

# schedule.find_hours(('CS', '1101'))
schedule.add_course(('CS', '3251'), 3)
schedule.add_course(('CS', '4269'), 4)
schedule.add_course(('CS', '1101'), 1)
schedule.remove_course(('CS', '1101'), 1)
schedule.move_course(('CS', '4269'), 4, 7)
schedule.clear()
schedule.planner([[('CS', '1101')],
                  [('CS', '2201'), ('EECE', '2116')],
                  [('CS', '3251'), ('CS', '3250')],
                  [('CS', '3281'), ('CS', '3270')],
                  [('CS', '3891'), ('CS', '3891'), ('CS', '4288')],
                  [('CS', '3860')],
                  [('CS', '4260'), ('CS', '3861')],
                  [('CS', '4269')]])
print(schedule)
