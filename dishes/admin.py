from django.contrib import admin

from .models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    list_editable = ("price",)
    search_fields = ("name", "category")
    list_filter = ("category",)
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("slug",)
