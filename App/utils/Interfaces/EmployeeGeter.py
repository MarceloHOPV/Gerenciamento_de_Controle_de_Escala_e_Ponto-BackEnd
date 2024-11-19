from abc import ABC, abstractmethod

class EmployeeGeter(ABC):
    @abstractmethod
    def get_employee(self, *args, **kwargs):
        pass
