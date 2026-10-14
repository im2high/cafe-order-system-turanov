"""Загрузка и сохранение JSON-файлов."""
import json
import os
from typing import List

from models.dishes import Dish, find_dish_by_id
from models.employees import Employee, find_employee_by_id
from models.orders import Order
from models.statuses import Status

DATA_DIR = "data"
DISHES_FILE = "data/dishes.json"
EMPLOYEES_FILE = "data/employees.json"
ORDERS_FILE = "data/orders.json"


def ensure_data_dir() -> None:
    """Создать папку data, если её ещё нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_dishes(filename: str = DISHES_FILE) -> List[Dish]:
    """Прочитать блюда из JSON."""
    ensure_data_dir()
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print("Ошибка загрузки блюд:", error)
        return []

    dishes = []
    for item in data:
        dish = Dish(item["id"], item["name"], item["price"], item["category"])
        dishes.append(dish)
    return dishes


def save_dishes(dishes: List[Dish], filename: str = DISHES_FILE) -> None:
    """Записать блюда в JSON. Объект → словарь."""
    ensure_data_dir()
    data = []
    for dish in dishes:
        data.append({
            "id": dish.id,
            "name": dish.name,
            "price": dish.price,
            "category": dish.category,
        })
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_employees(filename: str = EMPLOYEES_FILE) -> List[Employee]:
    """Прочитать сотрудников из JSON."""
    ensure_data_dir()
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print("Ошибка загрузки сотрудников:", error)
        return []

    employees = []
    for item in data:
        employee = Employee(item["id"], item["name"], item["position"])
        employees.append(employee)
    return employees


def save_employees(employees: List[Employee],
                   filename: str = EMPLOYEES_FILE) -> None:
    """Записать сотрудников в JSON."""
    ensure_data_dir()
    data = []
    for employee in employees:
        data.append({
            "id": employee.id,
            "name": employee.name,
            "position": employee.position,
        })
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_orders(dishes: List[Dish], employees: List[Employee],
                filename: str = ORDERS_FILE) -> List[Order]:
    """Загрузить заказы и восстановить связи с блюдами и сотрудниками."""
    ensure_data_dir()
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print("Ошибка загрузки заказов:", error)
        return []

    orders = []
    for item in data:
        employee = find_employee_by_id(employees, item["employee_id"])
        if employee is None:
            print(f"Сотрудник с id={item['employee_id']} не найден, "
                  f"заказ {item['id']} пропущен.")
            continue

        # Собираем список блюд заранее и передаём в конструктор Order
        items_list = []
        for dish_data in item.get("items", []):
            dish = find_dish_by_id(dishes, dish_data["dish_id"])
            if dish is not None:
                items_list.append({
                    "dish": dish,
                    "quantity": dish_data["quantity"],
                })

        order = Order(
            item["id"],
            employee,
            item["order_date"],
            items=items_list,
            status=item.get("status", Status.NEW),
        )
        orders.append(order)
    return orders


def save_orders(orders: List[Order], filename: str = ORDERS_FILE) -> None:
    """Сохранить заказы: объекты → id-шники."""
    ensure_data_dir()
    data = []
    for order in orders:
        items_data = []
        for item in order.items:
            items_data.append({
                "dish_id": item["dish"].id,
                "quantity": item["quantity"],
            })
        data.append({
            "id": order.id,
            "employee_id": order.employee.id,
            "order_date": order.order_date,
            "status": order.status,
            "items": items_data,
        })
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
