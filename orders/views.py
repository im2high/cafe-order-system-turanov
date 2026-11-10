from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import render

from dishes.models import Dish
from employees.models import Employee
from models.statuses import Status

from .models import Order, OrderItem


SORT_OPTIONS = {
    "newest": ("-order_date", "-pk"),
    "oldest": ("order_date", "pk"),
    "employee": ("employee__name", "-order_date", "-pk"),
}


def orders(request):
    search = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    employee_name = request.GET.get("employee", "").strip()
    hide_cancelled = request.GET.get("hide_cancelled") == "1"
    sort = request.GET.get("sort", "newest")
    if sort not in SORT_OPTIONS:
        sort = "newest"
    if status not in Status.DESCRIPTIONS:
        status = ""

    orders_list = Order.objects.select_related("employee")
    if status:
        orders_list = orders_list.filter(status=status)
    if employee_name:
        orders_list = orders_list.filter(employee__name__icontains=employee_name)
    if search:
        orders_list = orders_list.filter(
            Q(employee__name__icontains=search) | Q(items__dish__name__icontains=search)
        ).distinct()
    if hide_cancelled:
        orders_list = orders_list.exclude(status=Status.CANCELLED)
    orders_list = orders_list.order_by(*SORT_OPTIONS[sort])

    paginator = Paginator(orders_list, 10)
    page = paginator.get_page(request.GET.get("page"))
    context = {
        "page": page,
        "search": search,
        "status": status,
        "status_choices": Status.DESCRIPTIONS.items(),
        "employee_name": employee_name,
        "hide_cancelled": hide_cancelled,
        "sort": sort,
    }
    return render(request, "orders/order_list.html", context)


def order_detail(request, order_id):
    order = Order.objects.select_related("employee").filter(pk=order_id).first()
    items = []
    if order:
        items = order.items.select_related("dish").order_by("pk")

    return render(
        request,
        "orders/order_detail.html",
        {"order": order, "items": items},
        status=404 if order is None else 200,
    )


def statistics(request):
    status_stats = Order.objects.values("status").annotate(count=Count("pk")).order_by("status")
    top_dishes = (
        OrderItem.objects.values("dish_id", "dish__name")
        .annotate(total_quantity=Sum("quantity"))
        .order_by("-total_quantity", "dish_id")
    )
    average_price = Dish.objects.aggregate(average=Avg("price"))["average"]
    employee_stats = Employee.objects.annotate(order_count=Count("orders")).order_by(
        "-order_count", "name"
    )
    context = {
        "status_stats": status_stats,
        "top_dishes": top_dishes,
        "average_price": average_price,
        "employee_stats": employee_stats,
    }
    return render(request, "orders/statistics.html", context)
