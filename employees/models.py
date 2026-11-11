from django.db import models


class Employee(models.Model):
    name = models.CharField("Имя", max_length=200)
    position = models.CharField("Должность", max_length=100)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.name
