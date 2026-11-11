from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "position")
    search_fields = ("name", "position")
    list_filter = ("position",)
    ordering = ("name",)
    list_per_page = 20
