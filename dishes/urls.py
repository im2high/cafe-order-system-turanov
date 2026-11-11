from django.urls import path

from . import views

app_name = "dishes"

urlpatterns = [
    path("", views.dishes, name="list"),
    path("<int:dish_id>/<str:slug>/", views.dish_detail, name="detail_slug"),
    path("<int:dish_id>/", views.dish_detail, name="detail"),
]
