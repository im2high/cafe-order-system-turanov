from datetime import date

from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Q, Sum
from django.shortcuts import render

from dishes.models import Dish
from employees.models import Employee

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
    if status not in Order.Status.values:
        status = ""

    orders_list = Order.objects.all()
    if status:
        orders_list = orders_list.filter(status=status)
    if employee_name:
        orders_list = orders_list.filter(employee__name__icontains=employee_name)
    if search:
        orders_list = orders_list.filter(
            Q(employee__name__icontains=search) | Q(items__dish__name__icontains=search)
        ).distinct()
    if hide_cancelled:
        orders_list = orders_list.without_cancelled()
    orders_list = (
        orders_list.annotate(employee_name=F("employee__name"))
        .values("id", "order_date", "employee_name", "status")
        .order_by(*SORT_OPTIONS[sort])
    )

    paginator = Paginator(orders_list, 10)
    page = paginator.get_page(request.GET.get("page"))
    context = {
        "page": page,
        "search": search,
        "status": status,
        "status_choices": Order.Status.choices,
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
        OrderItem.objects.annotate(dish_name=F("dish__name"))
        .values("dish_id", "dish_name")
        .annotate(total_quantity=Sum("quantity"))
        .order_by("-total_quantity", "dish_id")
    )
    average_price = Dish.objects.aggregate(average=Avg("price"))["average"]
    employee_stats = Employee.objects.annotate(order_count=Count("orders")).order_by(
        "-order_count", "name"
    )
    order_totals = Order.objects.aggregate(
        total=Count("pk"),
        active=Count("pk", filter=Q(status__in=Order.Status.active_values())),
        completed=Count("pk", filter=Q(status=Order.Status.COMPLETED)),
        cancelled=Count("pk", filter=Q(status=Order.Status.CANCELLED)),
    )
    selected_date = request.GET.get("date", "")
    date_error = ""
    free_employees = None
    if selected_date:
        try:
            work_date = date.fromisoformat(selected_date)
        except ValueError:
            date_error = "Введите дату в формате ГГГГ-ММ-ДД."
        else:
            busy_employees = Order.objects.active().for_date(work_date).values("employee_id")
            free_employees = Employee.objects.exclude(pk__in=busy_employees).order_by("name")

    context = {
        "order_totals": order_totals,
        "selected_date": selected_date,
        "date_error": date_error,
        "free_employees": free_employees,
        "status_stats": status_stats,
        "top_dishes": top_dishes,
        "average_price": average_price,
        "employee_stats": employee_stats,
    }
    return render(request, "orders/statistics.html", context)
