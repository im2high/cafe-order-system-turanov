from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.orders, name="list"),
    path("<int:order_id>/", views.order_detail, name="detail"),
    path("create/", views.order_create, name="create"),
    path("<int:order_id>/edit/", views.order_edit, name="edit"),
    path("<int:order_id>/cancel/", views.order_cancel, name="cancel"),
    path("statistics/", views.statistics, name="statistics"),  # ← новое
]
