from Employee import Employee

class EmployeeSearch:
    def __init__(self, username: str | None = None, nameSearch: str | None = None) -> None:
        """Employee search object."""
        self.username = username
        self.nameSearch = nameSearch
        
    def matches(self, employee: Employee) -> bool:
        """Returns True if the given employee matches the search."""
        if self.username is not None and employee.username != self.username:
            return False
        # If employee search cannot be found as a substring (case insensitive) in the employee's full name, no match.
        if self.nameSearch is not None and employee.name.lower().find(self.nameSearch.lower()) == -1:
            return False
        
        return True