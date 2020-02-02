import sys
import readcsv as course_dictionary
from scheduler import course_scheduler
from collections import namedtuple
import unittest

class TestCourseScheduler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.course_dict = course_dictionary.create_course_dict()

        # a dictionary that includes an additional major: spanish
        cls.span_dict = add_span_major()

    def test_dictionary(self):
        # CODE PROVIDED BY DR. FISHER
        # Test to see if all prereqs are in the file.
        prereq_list = [single_course for vals in self.course_dict.values()
                       for some_prereqs in vals.prereqs for single_course in some_prereqs]
        for prereq in prereq_list:
            if prereq not in self.course_dict:
                print(prereq)
        for key in self.course_dict:
            #Test to see if every course has a term and credits.
            if not self.course_dict[key].terms or not self.course_dict[key].credits:
                print(key)
            #Test to see if a course's prereqs include the course itself
            if key in [course for prereq in self.course_dict[key].prereqs for course in prereq]:
                print(key);
        # Prints all the CS courses.
        # for key in self.course_dict:
        #     if key.program == 'CS':
        #         print(key, self.course_dict[key])
        # Prints the entire dictionary.
        # course_dictionary.print_dict(self.course_dict)
        # print(self.course_dict[('CS', 'open3')])

    def test_impossible_goal(self):
        # the scheduler should return an empty conjunction if conditions of the goal cannot be satisfied in four years
        # there are 100 total ECON and EDUC courses, so it is impossible to take all in 4 years
        all_econ_educ = [(key.program, key.designation) for key in self.course_dict
                         if (key.program == 'ECON' or key.program == 'EDUC')]
        plan = course_scheduler(self.course_dict, all_econ_educ, [])
        self.assertEqual(plan, ())

    def test_no_goal(self):
        plan = course_scheduler(self.course_dict, [], [])
        self.assertEqual(plan, ())

    def test_cs_major(self):
        # testing the scheduler when only the cs major is the goal and the student has no initial credit
        plan = course_scheduler(self.course_dict, [], [])
        split_plan = split_by_term(plan)
        for year in split_plan:
            for term in split_plan:
                credit = split_plan[year][term]['credits']
                # ensuring proper number of credits every term
                self.assertTrue(12 <= credit <= 18)

    def test_goal_satisfied(self):
        # testing the scheduler when the provided goal has already been satisfied
        plan = course_scheduler(self.course_dict, [('CS','1101')], [('CS','1101')])
        self.assertEqual(plan, ())

    def test_one_class_goal(self):
        # sum of credits must not be less than 12 per term
        plan = course_scheduler(self.course_dict, [('CS', '3250')], [])
        total_credits = 0
        self.assertTrue(total_credits >= 12)

    def test_initial_state(self):
        # testing the scheduler when the student has intial credit
        plan = course_scheduler(self.course_dict, [], [])
        self.assertEqual(plan, ())

    def test_spanish_major(self):
        plan = course_scheduler(self.course_dict, [], [])
        self.assertEqual(plan, ())

def split_by_term(plan):
    """
    a function that is helpful for many tests
    given a plan, returns a dictionary of scheduled courses organized by year and term
    """
    scheduled_by_term = {'Frosh': {'Fall': {'courses': [], 'credits': 0},'Spring': {'courses': [], 'credits': 0}},
                         'Soph': {'Fall': {'courses': [], 'credits': 0}, 'Spring': {'courses': [], 'credits': 0}},
                         'Junior': {'Fall': {'courses': [], 'credits': 0}, 'Spring': {'courses': [], 'credits': 0}},
                         'Senior': {'Fall': {'courses': [], 'credits': 0}, 'Spring': {'courses': [], 'credits': 0}}}

    for scheduled in plan:
        year = scheduled[1][0]
        term = scheduled[1][1]
        course = scheduled[0]
        credit = scheduled[2]
        scheduled_by_term[year][term]['courses'].append(course)
        scheduled_by_term[year][term]['hours'] += credit

    return scheduled_by_term

def add_span_major():
    """
    returns the course dictionary with the spanish major added
    """
    span_dict = course_dictionary.create_course_dict()
    Course = namedtuple('Course', 'program, designation')
    CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')

    # Core requirements: 3301W, 3302, and 3303
    core_course = Course('SPAN', 'core')
    core_info = CourseInfo(0, 'Spring, Fall', 'SPAN3301W SPAN3302 SPAN3303')
    span_dict[core_course] = core_info

    # Literature: 9 credit hours from courses numbered 4400–4980 or 3835, or 3893
    literature_course = Course('SPAN', 'literature')
    literature_info = CourseInfo(0, 'Spring, Fall', 'SPANliterature1 SPANliterature2 SPANliterature3')
    span_dict[literature_course] = literature_info

    lit1_course = Course('SPAN', 'literature1')
    lit1_info = CourseInfo(0, 'Spring, Fall', 'SPAN4405,SPAN4420,SPAN4425,SPAN4620,SPAN4670,SPAN4750,SPAN4760,SPAN4415,SPAN4450,SPAN4465,SPAN4475,SPAN4550,SPAN4740,SPAN4355,SPAN4640,SPAN4730,SPAN4741,SPAN4400,SPAN4440')
    span_dict[lit1_course] = lit1_info

    lit2_course = Course('SPAN', 'literature2')
    lit2_info = CourseInfo(0, 'Spring, Fall', 'SPAN4405,SPAN4420,SPAN4425,SPAN4620,SPAN4670,SPAN4750,SPAN4760,SPAN4415,SPAN4450,SPAN4465,SPAN4475,SPAN4550,SPAN4740,SPAN4355,SPAN4640,SPAN4730,SPAN4741,SPAN4400,SPAN4440')
    span_dict[lit2_course] = lit2_info

    lit3_course = Course('SPAN', 'literature3')
    lit3_info = CourseInfo(0, 'Spring, Fall', 'SPAN4405,SPAN4420,SPAN4425,SPAN4620,SPAN4670,SPAN4750,SPAN4760,SPAN4415,SPAN4450,SPAN4465,SPAN4475,SPAN4550,SPAN4740,SPAN4355,SPAN4640,SPAN4730,SPAN4741,SPAN4400,SPAN4440')
    span_dict[lit3_course] = lit3_info

    # Linguistics: 3 credit hours from courses numbered 4300–4360, or 3892
    linguistic_course = Course('SPAN', 'linguistic')
    linguistic_info = CourseInfo(0, 'Spring, Fall', 'SPAN3892,SPAN4315,SPAN4320,SPAN4340,SPAN4345,SPAN4310,SPAN4335,SPAN4355,SPAN4325')
    span_dict[linguistic_course] = linguistic_info

    # Electives: 9 credit hours from courses numbered 3320–3835 or 3891-4980
    elective_course = Course('SPAN', 'electives')
    elective_info = CourseInfo(0, 'Spring, Fall', 'SPANelectives1 SPANelectives2 SPANelectives3')
    span_dict[elective_course] = elective_info

    elective1_course = Course('SPAN', 'electives1')
    elective1_info = CourseInfo(0, 'Spring, Fall', 'SPAN3340,SPAN3345,SPAN3355,SPAN3360,SPAN3830,SPAN3365,SPAN3835,SPAN3325,SPAN3330,SPAN3350')
    span_dict[elective1_course] = elective1_info

    elective2_course = Course('SPAN', 'electives2')
    elective2_info = CourseInfo(0, 'Spring, Fall', 'SPAN3340,SPAN3345,SPAN3355,SPAN3360,SPAN3830,SPAN3365,SPAN3835,SPAN3325,SPAN3330,SPAN3350')
    span_dict[elective2_course] = elective2_info

    elective3_course = Course('SPAN', 'electives3')
    elective3_info = CourseInfo(0, 'Spring, Fall', 'SPAN3340,SPAN3345,SPAN3355,SPAN3360,SPAN3830,SPAN3365,SPAN3835,SPAN3325,SPAN3330,SPAN3350')
    span_dict[elective3_course] = elective3_info

    major_course = Course('SPAN', 'major')
    major_info = CourseInfo(0, 'Spring, Fall', 'SPANcore SPANliterature SPANlinguistic SPANelectives')
    span_dict[major_course] = major_info

    return span_dict

if __name__ == "__main__":
    unittest.main()