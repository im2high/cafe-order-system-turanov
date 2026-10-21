from django.shortcuts import render

from models.employees import find_employee_by_id
from storage import load_employees


def employees(request):
    employees_list = load_employees("data/employees.json")
    context = {"employees": employees_list}
    return render(request, "employees/employee_list.html", context)


def employee_detail(request, employee_id):
    employees_list = load_employees("data/employees.json")
    employee = find_employee_by_id(employees_list, employee_id)
    context = {"employee": employee}
    return render(
        request,
        "employees/employee_detail.html",
        context,
        status=404 if employee is None else 200,
    )
