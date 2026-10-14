"""Страницы блюд."""
from django.http import HttpResponse

from homepage.views import page
from models.dishes import find_dish_by_id
from storage import load_dishes


def dishes(request):
    """Список блюд."""
    items = ""
    for dish in load_dishes("data/dishes.json"):
        text = f"{dish.name} — {dish.price:.2f} руб."
        items += (
            f'<li class="list-group-item">'
            f'<a href="/dishes/{dish.id}/">{text}</a>'
            f'</li>'
        )
    content = f"""
    <h1>Блюда</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Кафе — блюда", content))


def dish_detail(request, dish_id):
    """Одно блюдо."""
    dishes_list = load_dishes("data/dishes.json")
    dish = find_dish_by_id(dishes_list, dish_id)
    if dish is None:
        content = """
        <h1 class="text-danger">Блюдо не найдено</h1>
        <a href="/dishes/" class="btn btn-outline-secondary">
          ← к списку блюд
        </a>
        """
        return HttpResponse(
            page("Блюдо не найдено", content),
            status=404,
        )

    content = f"""
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{dish.name}</h5>
        <p class="card-text"><strong>ID:</strong> {dish.id}</p>
        <p class="card-text"><strong>Цена:</strong>
          {dish.price:.2f} руб.</p>
        <p class="card-text"><strong>Категория:</strong>
          {dish.category}</p>
        <a href="/dishes/" class="btn btn-outline-secondary">
          ← к списку блюд
        </a>
      </div>
    </div>
    """
    return HttpResponse(page(dish.name, content))
