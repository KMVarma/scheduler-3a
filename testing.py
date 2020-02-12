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

    def test_proper_terms(self):
        # ensuring the correct years and terms are included
        # this goal should result in a 3-semester plan
        plan = course_scheduler(self.course_dict, [('MATH', '4110')], [])
        split_plan = split_by_term(plan)
        years = list(split_plan.keys())
        self.assertNotEqual(split_plan['Frosh']['Fall']['courses'], [])
        self.assertNotEqual(split_plan['Frosh']['Spring']['courses'], [])
        self.assertNotEqual(split_plan['Soph']['Fall']['courses'], [])
        self.assertEqual(split_plan['Soph']['Spring']['courses'], [])
        self.assertEqual(split_plan['Junior']['Fall']['courses'], [])
        self.assertEqual(split_plan['Junior']['Spring']['courses'], [])
        self.assertEqual(split_plan['Senior']['Fall']['courses'], [])
        self.assertEqual(split_plan['Senior']['Spring']['courses'], [])

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
        plan = course_scheduler(self.course_dict, [('CS', '1101'), ('SPAN', '1102'), ('SPAN', '3325')],
                                [('SPAN', '1101')])
        # the prereq for SPAN1102 is already satisfied so neither of its prereqs should be in the plan
        for course in plan:
            self.assertNotEqual(course[0], ('SPAN', '1101'))
            self.assertNotEqual(course[0], ('SPAN', '1100'))

    def test_simple_plan(self):
        # in this case, there is no ambiguity in the optimal terms to schedule the goal and its prereqs in
        plan = course_scheduler(self.course_dict, [('MATH', '2410')], [])
        split_plan = split_by_term(plan)
        self.assertTrue(('MATH', '1200') in split_plan['Frosh']['Fall']['courses']
                        or ('MATH', '1300') in split_plan['Frosh']['Fall']['courses'])
        if ('MATH', '1200') in split_plan['Frosh']['Fall']['courses']:
            self.assertTrue(('MATH', '1201') in split_plan['Frosh']['Spring']['courses'])
            self.assertTrue(('MATH', '2200') in split_plan['Soph']['Fall']['courses'])
            self.assertTrue(('MATH', '2300') in split_plan['Soph']['Spring']['courses'])
            self.assertTrue(('MATH', '2410') in split_plan['Junior']['Fall']['courses'])
        if ('MATH', '1300') in split_plan['Frosh']['Fall']['courses']:
            self.assertTrue(('MATH', '1301') in split_plan['Frosh']['Spring']['courses'])
            self.assertTrue(('MATH', '2300') in split_plan['Soph']['Fall']['courses'])
            self.assertTrue(('MATH', '2410') in split_plan['Soph']['Spring']['courses'])

    def test_logistics(self):
        # ensure that all scheduled courses are actual courses (ie. are not higher level requirements or empty)
        # and are offered during the semester they are scheduled
        plan = course_scheduler(self.course_dict, [('CS', 'major')], [])
        split_plan = split_by_term(plan)
        Course = namedtuple('Course', 'program, designation')
        for year in split_plan:
            for term in year:
                for course in term['courses']:
                    key = Course(course[0], course[1])
                    terms = self.course_dict[key].terms
                    self.assertTrue(term in terms)
                    self.assertNotEqual(self.course_dict[key].credits, 0)
                credit = split_plan[year][term]['credits']
                self.assertTrue(12 <= credit <= 18)

    def test_5_credits(self):
        # goal of only 4 courses, but cannot all fit in one term since they're all 5-credit
        plan = course_scheduler(self.course_dict,
                                 [('SPAN', '1100'), ('SPAN', '1101'), ('SPAN', '1103'), ('SPAN', '2203')], [])
        split_plan = split_by_term(plan)
        self.assertNotEqual(split_plan['Frosh']['Fall']['courses'], [])
        self.assertNotEqual(split_plan['Frosh']['Spring']['courses'], [])
        self.assertEqual(split_plan['Soph']['Fall']['courses'], [])
        self.assertEqual(split_plan['Soph']['Spring']['courses'], [])
        self.assertEqual(split_plan['Junior']['Fall']['courses'], [])
        self.assertEqual(split_plan['Junior']['Spring']['courses'], [])
        self.assertEqual(split_plan['Senior']['Fall']['courses'], [])
        self.assertEqual(split_plan['Senior']['Spring']['courses'], [])

    def test_spanish_major(self):
        # more thoroughly testing the spanish major plan (according to the catalog and project spec it is very simple)
        plan = course_scheduler(self.span_dict, [('SPAN', 'major')], [])
        split_plan = split_by_term(plan)
        # ensure proper number of credits each semester
        for year in split_plan:
            for term in year:
                self.assertTrue(12 <= term['credits'] <= 18)
        # check that all core requirements are satisfied
        self.assertTrue((('SPAN', '3301W'), ('Fall', 'Frosh'), 3) in plan)
        self.assertTrue((('SPAN', '3302'), ('Spring', 'Frosh'), 3) in plan)
        self.assertTrue((('SPAN', '3303'), ('Fall', 'Soph'), 3) in plan)
        Course = namedtuple('Course', 'program, designation')
        literature_req = self.span_dict[Course('SPAN', 'literature1')].prereqs
        literature_count = 3
        lingusitc_req = self.span_dict[Course('SPAN', 'linguistic')].prereqs
        lingusitc_count = 1
        electives_req = self.span_dict[Course('SPAN', 'electives1')].prereqs
        electives_count = 3
        courses = []
        for scheduled in plan:
            course = scheduled[0]
            courses.append(course)
            full_name = course[0] + course[1]
            if full_name in literature_req:
                literature_count -= 1
            if full_name in lingusitc_req:
                electives_count -= 1
            if full_name in electives_req:
                electives_count -= 1
        # check that all non-core requirements are satisfied
        self.assertTrue(literature_count <= 0)
        self.assertTrue(lingusitc_count <= 0)
        self.assertTrue(electives_count <= 0)
        # check that there are no duplicates
        self.assertNotEqual(len(courses), len(set(courses)))

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
        year = scheduled[1][1]
        term = scheduled[1][0]
        course = scheduled[0]
        credit = scheduled[2]
        scheduled_by_term[year][term]['courses'].append(course)
        scheduled_by_term[year][term]['credits'] += credit

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