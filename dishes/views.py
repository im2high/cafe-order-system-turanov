from django.shortcuts import render

from models.dishes import find_dish_by_id
from storage import load_dishes


def dishes(request):
    dishes_list = load_dishes("data/dishes.json")
    context = {"dishes": dishes_list}
    return render(request, "dishes/dish_list.html", context)


def dish_detail(request, dish_id):
    dishes_list = load_dishes("data/dishes.json")
    dish = find_dish_by_id(dishes_list, dish_id)
    context = {"dish": dish}
    return render(
        request,
        "dishes/dish_detail.html",
        context,
        status=404 if dish is None else 200,
    )
