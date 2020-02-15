class Course:
    def __init__(self, name, prereqs, terms, hours):
        self.name = name
        self.prereqs = prereqs
        self.terms = terms
        self.hours = hours

    def __str__(self):
        return str(self.name ) # + ' ' + str(self.hours)

    def __repr__(self):
        return self.__str__()