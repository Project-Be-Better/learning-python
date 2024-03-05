class FirstClass:
    """Defines class object"""

    def setData(self, value):
        self.data = value

    def display(self):
        return self.data


class Employee:

    def __init__(self, name, last) -> None:
        self.name = name
        self.last = last


class Supervisor(Employee):

    def __init__(self, name, last, password) -> None:
        super().__init__(name, last)
        self.password = password


class Chef(Employee):

    def leave_request(self, days):
        return f"May I take leave for ${days}"
