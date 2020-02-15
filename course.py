from utils import get_course_info, format_prereqs

class Course:
    def __init__(self, name, prereqs, terms, hours, satisfies=None):
        if satisfies is None:
            satisfies = []
        self.name = name
        self.prereqs = prereqs
        self.terms = terms
        self.hours = hours
        self.satisfies = satisfies

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Course):
            return self.name == other.name
        if isinstance(other, str):
            return str(self.name) == other
        if isinstance(other, tuple):
            return self.name == other
        return False

    @classmethod
    def from_name(cls, name):
        info = get_course_info(name)
        prereqs = format_prereqs(info.prereqs)
        terms = info.terms
        hours = int(info.credits)
        return cls(name, prereqs, terms, hours)
