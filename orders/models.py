from django.db import models

from models.statuses import Status as OldStatus


class OrderStatus(models.TextChoices):
    NEW = OldStatus.NEW, OldStatus.DESCRIPTIONS[OldStatus.NEW]
    COOKING = OldStatus.COOKING, OldStatus.DESCRIPTIONS[OldStatus.COOKING]
    READY = OldStatus.READY, OldStatus.DESCRIPTIONS[OldStatus.READY]
    COMPLETED = OldStatus.COMPLETED, OldStatus.DESCRIPTIONS[OldStatus.COMPLETED]
    CANCELLED = OldStatus.CANCELLED, OldStatus.DESCRIPTIONS[OldStatus.CANCELLED]

    @classmethod
    def active_values(cls):
        return (cls.NEW, cls.COOKING, cls.READY)


class OrderQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=OrderStatus.active_values())

    def cancelled(self):
        return self.filter(status=OrderStatus.CANCELLED)

    def completed(self):
        return self.filter(status=OrderStatus.COMPLETED)

    def for_date(self, order_date):
        return self.filter(order_date=order_date)

    def without_cancelled(self):
        return self.exclude(status=OrderStatus.CANCELLED)


class Order(models.Model):
    Status = OrderStatus

    objects = OrderQuerySet.as_manager()

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Сотрудник",
    )
    order_date = models.DateField("Дата заказа")
    status = models.CharField(
        "Статус", max_length=20, choices=Status.choices, default=Status.NEW
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ"
    )
    dish = models.ForeignKey(
        "dishes.Dish",
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name="Блюдо",
    )
    quantity = models.PositiveIntegerField("Количество")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    @property
    def total(self):
        return self.dish.price * self.quantity

    def __str__(self):
        return f"{self.dish.name} × {self.quantity}"
