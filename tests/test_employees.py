from models.employees import (
    Employee, add_employee, find_employee_by_id,
)


def test_employee_creation():
    employee = Employee(1, "Анна", "Официант")
    assert employee.id == 1
    assert employee.name == "Анна"
    assert employee.position == "Официант"


def test_employee_str():
    employee = Employee(1, "Анна", "Официант")
    assert "Анна" in str(employee)


def test_add_employee():
    employees = []
    add_employee(employees, 1, "Анна", "Официант")
    assert len(employees) == 1


def test_find_employee_by_id():
    employees = []
    add_employee(employees, 1, "Анна", "Официант")
    assert find_employee_by_id(employees, 1) is employees[0]
    assert find_employee_by_id(employees, 99) is None