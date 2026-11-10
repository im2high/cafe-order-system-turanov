from django.shortcuts import render

from .models import Employee


def employees(request):
    employees_list = Employee.objects.order_by("name")
    return render(request, "employees/employee_list.html", {"employees": employees_list})


def employee_detail(request, employee_id):
    employee = Employee.objects.filter(pk=employee_id).first()
    return render(
        request,
        "employees/employee_detail.html",
        {"employee": employee},
        status=404 if employee is None else 200,
    )
