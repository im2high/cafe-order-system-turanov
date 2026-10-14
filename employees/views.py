"""Страницы сотрудников."""
from django.http import HttpResponse

from homepage.views import page
from models.employees import find_employee_by_id
from storage import load_employees


def employees(request):
    """Список сотрудников."""
    items = ""
    for employee in load_employees("data/employees.json"):
        text = f"{employee.name} — {employee.position}"
        items += (
            f'<li class="list-group-item">'
            f'<a href="/employees/{employee.id}/">{text}</a>'
            f'</li>'
        )
    content = f"""
    <h1>Сотрудники</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Кафе — сотрудники", content))


def employee_detail(request, employee_id):
    """Один сотрудник."""
    employees_list = load_employees("data/employees.json")
    employee = find_employee_by_id(employees_list, employee_id)
    if employee is None:
        content = """
        <h1 class="text-danger">Сотрудник не найден</h1>
        <a href="/employees/" class="btn btn-outline-secondary">
          ← к списку сотрудников
        </a>
        """
        return HttpResponse(
            page("Сотрудник не найден", content),
            status=404,
        )

    content = f"""
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{employee.name}</h5>
        <p class="card-text"><strong>ID:</strong> {employee.id}</p>
        <p class="card-text"><strong>Должность:</strong>
          {employee.position}</p>
        <a href="/employees/" class="btn btn-outline-secondary">
          ← к списку сотрудников
        </a>
      </div>
    </div>
    """
    return HttpResponse(page(employee.name, content))
