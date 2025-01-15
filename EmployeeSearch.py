from Employee import Employee

class EmployeeSearch:
    def __init__(self, username: str | None = None, nameSearch: str | None = None) -> None:
        self.username = username
        self.nameSearch = nameSearch
        
    def matches(self, employee: Employee) -> bool:
        if employee.username != self.username and self.username is not None:
            return False
        if self.nameSearch is not None and employee.name.lower().find(self.nameSearch.lower()) == -1:
            return False
        
        return True