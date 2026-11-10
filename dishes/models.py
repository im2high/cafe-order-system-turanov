from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name
