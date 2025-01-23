from Customer import Customer

class CustomerSearch:
    def __init__(self, nameSearch: str | None) -> None:
        self.nameSearch = nameSearch
        
    def matches(self, customer: Customer) -> bool:
        if self.nameSearch is not None and f"{customer.fName} {customer.sName}".lower().find(self.nameSearch.lower()) == -1:
            return False
        
        return True