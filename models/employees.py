class Employee:

    def __init__(self, employee_id: int, name: str, position: str) -> None:
        self.id = employee_id
        self.name = name
        self.position = position

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} — {self.position}"


def add_employee(employees: list[Employee], employee_id: int,
                 name: str, position: str) -> Employee:
    employee = Employee(employee_id, name, position)
    employees.append(employee)
    return employee


def find_employee_by_id(employees: list[Employee],
                        employee_id: int) -> Employee | None:
    for employee in employees:
        if employee.id == employee_id:
            return employee
    return None


def show_employees(employees: list[Employee]) -> None:
    if len(employees) == 0:
        print("Список сотрудников пуст.")
        return
    for employee in employees:
        print(employee)