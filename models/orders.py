"""Работа с заказами."""
from typing import List, Optional

from models.dishes import Dish
from models.employees import Employee
from models.statuses import Status


class Order:
    """Заказ в кафе."""

    def __init__(
        self,
        order_id: int,
        employee: Employee,
        order_date: str,
        items: Optional[List[dict]] = None,
        status: str = Status.NEW,
    ) -> None:
        self.id = order_id
        self.employee = employee
        self.order_date = order_date
        self.status = status
        if items is None:
            self.items = []
        else:
            self.items = items

    def add_item(self, dish: Dish, quantity: int) -> None:
        """Добавить блюдо в заказ."""
        self.items.append({"dish": dish, "quantity": quantity})

    def calculate_total(self) -> float:
        """Сумма заказа. Обычный цикл for."""
        total = 0.0
        for item in self.items:
            dish = item["dish"]
            quantity = item["quantity"]
            total = total + dish.price * quantity
        return total

    def cancel(self) -> bool:
        """Отменить заказ, если статус позволяет."""
        if Status.can_cancel(self.status):
            self.status = Status.CANCELLED
            return True
        return False

    def get_status_description(self) -> str:
        """Строка с описанием статуса."""
        return Status.get_description(self.status)

    def __str__(self) -> str:
        """Текстовое представление заказа."""
        items_str = ""
        for item in self.items:
            dish = item["dish"]
            quantity = item["quantity"]
            items_str = items_str + f"{dish.name} x{quantity}, "
        items_str = items_str.rstrip(", ")
        if items_str == "":
            items_str = "нет блюд"

        return (
            f"Заказ №{self.id} от {self.order_date}\n"
            f"  Сотрудник: {self.employee.name}\n"
            f"  Блюда: {items_str}\n"
            f"  Сумма: {self.calculate_total():.2f} руб.\n"
            f"  Статус: {self.get_status_description()}"
        )


def create_order(orders: List[Order], order_id: int,
                 employee: Employee, order_date: str) -> Order:
    """Создать заказ и добавить в список."""
    order = Order(order_id, employee, order_date)
    orders.append(order)
    return order


def find_order_by_id(orders: List[Order], order_id: int) -> Optional[Order]:
    """Найти заказ по id."""
    for order in orders:
        if order.id == order_id:
            return order
    return None


def cancel_order(orders: List[Order], order_id: int) -> bool:
    """Найти заказ и попробовать его отменить."""
    order = find_order_by_id(orders, order_id)
    if order is None:
        return False
    return order.cancel()


def filter_orders_by_status(orders: List[Order], status: str) -> List[Order]:
    """Оставить заказы с нужным статусом."""
    result = []
    for order in orders:
        if order.status == status:
            result.append(order)
    return result


def get_orders_statistics(orders: List[Order]) -> dict:
    """Собрать статистику. Без sum() и генераторов."""
    stats = {
        "total_orders": 0,
        "total_revenue": 0.0,
        "by_status": {},
    }
    for order in orders:
        stats["total_orders"] = stats["total_orders"] + 1
        current_total = order.calculate_total()
        stats["total_revenue"] = stats["total_revenue"] + current_total
        current_status = order.status
        if current_status in stats["by_status"]:
            stats["by_status"][current_status] += 1
        else:
            stats["by_status"][current_status] = 1
    return stats


def show_orders(orders: List[Order]) -> None:
    """Напечатать все заказы."""
    if len(orders) == 0:
        print("Список заказов пуст.")
        return
    for order in orders:
        print(order)
        print("-" * 40)
