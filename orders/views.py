from datetime import date

from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Avg, Count, F, Q, Sum
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from dishes.models import Dish
from employees.models import Employee

from .forms import OrderFilterForm, OrderForm, OrderItemFormSet
from .models import Order, OrderItem


SORT_OPTIONS = {
    "newest": ("-order_date", "-pk"),
    "oldest": ("order_date", "pk"),
    "employee": ("employee__name", "-order_date", "-pk"),
}


def orders(request):
    filters = params = request.GET.copy()
    params.setdefault("sort", "oldest")
    filters = OrderFilterForm(params)
    filters.is_valid()
    data = filters.cleaned_data
    sort = data.get("sort") or "oldest"

    orders_list = Order.objects.all()
    if data.get("status"):
        orders_list = orders_list.filter(status=data["status"])
    if data.get("employee"):
        orders_list = orders_list.filter(employee__name__icontains=data["employee"])
    if data.get("date"):
        orders_list = orders_list.for_date(data["date"])
    if data.get("q"):
        search = data["q"]
        orders_list = orders_list.filter(
            Q(employee__name__icontains=search) | Q(items__dish__name__icontains=search)
        ).distinct()
    if data.get("hide_cancelled"):
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
        "filters": filters,
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


@staff_member_required
def order_create(request):
    return order_form(request, Order())


@staff_member_required
@transaction.atomic
def order_edit(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if not order.can_edit():
        return HttpResponseBadRequest("Изменить можно только активный заказ.")
    return order_form(request, order)


def order_form(request, order):
    data = request.POST if request.method == "POST" else None
    form = OrderForm(data, instance=order)
    items = OrderItemFormSet(data, instance=order)
    if request.method == "POST":
        with transaction.atomic():
            form_valid = form.is_valid()
            items_valid = items.is_valid()
            if form_valid and items_valid:
                saved_order = form.save()
                items.instance = saved_order
                items.save()
                return redirect("orders:detail", order_id=saved_order.pk)

    return render(request, "orders/order_form.html", {"form": form, "items": items})


@require_POST
@staff_member_required
def order_cancel(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if not order.cancel():
        return HttpResponseBadRequest("Отменить можно только новый или готовящийся заказ.")
    return redirect("orders:detail", order_id=order.pk)


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
