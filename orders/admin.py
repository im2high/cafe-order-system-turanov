from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("dish",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "order_date", "employee", "status")
    list_display_links = ("id", "order_date")
    list_filter = ("status", "order_date", "employee")
    search_fields = ("=id", "employee__name", "items__dish__name")
    ordering = ("-order_date", "-pk")
    list_select_related = ("employee",)
    list_per_page = 20
    autocomplete_fields = ("employee",)
    inlines = (OrderItemInline,)
