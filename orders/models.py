from django.db import models

from models.statuses import Status


class Order(models.Model):
    employee = models.ForeignKey(
        "employees.Employee", on_delete=models.PROTECT, related_name="orders"
    )
    order_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=Status.DESCRIPTIONS, default=Status.NEW
    )

    def __str__(self):
        return f"Заказ №{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    dish = models.ForeignKey(
        "dishes.Dish", on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveIntegerField()

    @property
    def total(self):
        return self.dish.price * self.quantity

    def __str__(self):
        return f"{self.dish.name} × {self.quantity}"
