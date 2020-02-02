import readcsv
import planner

# Creates course dict and prints first 5 entries
course_dict = readcsv.create_course_dict()
readcsv.print_dict(course_dict, 5)

def course_scheduler (course_descriptions, goal_conditions, initial_state):
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
