class Employee:
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay

    def get_info(self):
        return f"{self.name} earns {self.pay}"

    def apply_raise(self):
        self.pay = int(self.pay * 1.04)


class Manager(Employee):
    def __init__(self, name, pay, team):
        super().__init__(name, pay)  # Employee handles name and pay
        self.team = team             # Manager's own extra thing

    def add_to_team(self, person):
        self.team.append(person)

    def get_info(self):              # overrides Employee's version
        base = super().get_info()    # reuse Employee's version as starting point
        return f"{base} | manages {self.team}"


class Developer(Employee):
    def __init__(self, name, pay, language):
        super().__init__(name, pay)
        self.language = language
    # no get_info, no apply_raise — uses Employee's versions automatically


m1 = Manager("Talim", 70000, ["Sadi", "Rafi"])
d1 = Developer("Nafi", 50000, "Python")

print(m1.get_info())   # Manager's overridden version
print(d1.get_info())   # Employee's version, used automatically

m1.apply_raise()       # inherited from Employee
print(m1.pay)

m1.add_to_team("Nafi")
print(m1.get_info())