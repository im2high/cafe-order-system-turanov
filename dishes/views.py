from django.shortcuts import get_object_or_404, render

from .models import Dish


def dishes(request):
    search = request.GET.get("q", "").strip()
    dishes_list = Dish.objects.order_by("name")
    if search:
        dishes_list = dishes_list.filter(name__icontains=search)

    return render(request, "dishes/dish_list.html", {"dishes": dishes_list, "search": search})


def dish_detail(request, dish_id, slug=None):
    if slug is None:
        dish = Dish.objects.filter(pk=dish_id).first()
    else:
        dish = get_object_or_404(Dish, pk=dish_id, slug=slug)
    return render(
        request,
        "dishes/dish_detail.html",
        {"dish": dish},
        status=404 if dish is None else 200,
    )
