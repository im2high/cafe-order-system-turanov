from django.shortcuts import render

from models.orders import find_order_by_id
from storage import load_dishes, load_employees, load_orders


def orders(request):
    dishes_list = load_dishes("data/dishes.json")
    employees_list = load_employees("data/employees.json")
    orders_list = load_orders(
        dishes_list, employees_list, "data/orders.json",
    )
    context = {"orders": orders_list}
    return render(request, "orders/order_list.html", context)


def order_detail(request, order_id):
    dishes_list = load_dishes("data/dishes.json")
    employees_list = load_employees("data/employees.json")
    orders_list = load_orders(
        dishes_list, employees_list, "data/orders.json",
    )
    order = find_order_by_id(orders_list, order_id)
    context = {"order": order}
    return render(
        request,
        "orders/order_detail.html",
        context,
        status=404 if order is None else 200,
    )
