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
        return str(self.name)  # + ' ' + str(self.hours)

    def __repr__(self):
        return self.__str__()
