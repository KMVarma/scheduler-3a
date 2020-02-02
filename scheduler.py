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
print(schedule)
