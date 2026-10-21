"""Страницы сотрудников через SQLite."""
import sqlite3

from django.shortcuts import render

DB_PATH = "data/cafe.sqlite"


def employees(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    employees_list = conn.execute(
        "SELECT id, name, position FROM employees ORDER BY name"
    ).fetchall()
    conn.close()
    return render(request, "employees/employee_list.html", {"employees": employees_list})


def employee_detail(request, employee_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    employee = conn.execute(
        "SELECT id, name, position FROM employees WHERE id = ?",
        [employee_id],
    ).fetchone()
    conn.close()
    return render(
        request,
        "employees/employee_detail.html",
        {"employee": employee},
        status=404 if employee is None else 200,
    )
