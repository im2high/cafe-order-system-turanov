"""Страницы заказов."""
from django.http import HttpResponse

from homepage.views import page
from models.orders import find_order_by_id
from storage import load_dishes, load_employees, load_orders


def orders(request):
    """Список заказов."""
    dishes_list = load_dishes("data/dishes.json")
    employees_list = load_employees("data/employees.json")
    orders_list = load_orders(
        dishes_list, employees_list, "data/orders.json",
    )

    items = ""
    for order in orders_list:
        total = order.calculate_total()
        text = (
            f"Заказ №{order.id} от {order.order_date} — "
            f"{total:.2f} руб."
        )
        items += (
            f'<li class="list-group-item">'
            f'<a href="/orders/{order.id}/">{text}</a>'
            f'</li>'
        )
    content = f"""
    <h1>Заказы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Кафе — заказы", content))


def order_detail(request, order_id):
    """Один заказ."""
    dishes_list = load_dishes("data/dishes.json")
    employees_list = load_employees("data/employees.json")
    orders_list = load_orders(
        dishes_list, employees_list, "data/orders.json",
    )

    order = find_order_by_id(orders_list, order_id)
    if order is None:
        content = """
        <h1 class="text-danger">Заказ не найден</h1>
        <a href="/orders/" class="btn btn-outline-secondary">
          ← к списку заказов
        </a>
        """
        return HttpResponse(
            page("Заказ не найден", content),
            status=404,
        )

    items_str = ""
    for item in order.items:
        dish = item["dish"]
        quantity = item["quantity"]
        items_str += f"{dish.name} x{quantity}, "
    items_str = items_str.rstrip(", ")
    if items_str == "":
        items_str = "нет блюд"

    status_text = order.get_status_description()

    content = f"""
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Заказ №{order.id}</h5>
        <p class="card-text"><strong>Дата:</strong>
          {order.order_date}</p>
        <p class="card-text"><strong>Сотрудник:</strong>
          {order.employee.name}</p>
        <p class="card-text"><strong>Блюда:</strong>
          {items_str}</p>
        <p class="card-text"><strong>Сумма:</strong>
          {order.calculate_total():.2f} руб.</p>
        <p class="card-text"><strong>Статус:</strong>
          {status_text}</p>
        <a href="/orders/" class="btn btn-outline-secondary">
          ← к списку заказов
        </a>
      </div>
    </div>
    """
    return HttpResponse(page(f"Заказ №{order.id}", content))
