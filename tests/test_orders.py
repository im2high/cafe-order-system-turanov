from models.dishes import Dish
from models.employees import Employee
from models.orders import (
    Order, create_order, find_order_by_id, cancel_order,
    filter_orders_by_status, get_orders_statistics,
)
from models.statuses import Status


def make_order():
    """Вспомогательная функция — создать заказ с одним блюдом."""
    employee = Employee(1, "Анна", "Официант")
    order = Order(1, employee, "2026-09-15")
    order.add_item(Dish(1, "Капучино", 180.5, "Напитки"), 2)
    return order


def test_order_creation():
    order = make_order()
    assert order.id == 1
    assert order.status == Status.NEW
    assert len(order.items) == 1


def test_order_total():
    order = make_order()
    assert order.calculate_total() == 361.0


def test_order_cancel():
    order = make_order()
    assert order.cancel() is True
    assert order.status == Status.CANCELLED


def test_order_cannot_cancel_completed():
    order = make_order()
    order.status = Status.COMPLETED
    assert order.cancel() is False


def test_find_order_by_id():
    orders = []
    employee = Employee(1, "Анна", "Официант")
    create_order(orders, 1, employee, "2026-09-15")
    assert find_order_by_id(orders, 1) is orders[0]
    assert find_order_by_id(orders, 99) is None


def test_filter_orders_by_status():
    orders = []
    employee = Employee(1, "Анна", "Официант")
    create_order(orders, 1, employee, "2026-09-15")
    create_order(orders, 2, employee, "2026-09-16")
    orders[1].status = Status.COMPLETED
    result = filter_orders_by_status(orders, Status.NEW)
    assert len(result) == 1


def test_statistics():
    orders = []
    employee = Employee(1, "Анна", "Официант")
    order = create_order(orders, 1, employee, "2026-09-15")
    order.add_item(Dish(1, "Капучино", 180.5, "Напитки"), 2)
    stats = get_orders_statistics(orders)
    assert stats["total_orders"] == 1
    assert stats["total_revenue"] == 361.0