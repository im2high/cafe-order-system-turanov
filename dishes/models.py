from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Dish(models.Model):
    name = models.CharField("Название", max_length=200)
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2)
    category = models.CharField("Категория", max_length=100)

    slug = models.SlugField("Часть адреса", max_length=200, allow_unicode=True, blank=True)

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)[:200] or "dish"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if not self.slug:
            return reverse("dishes:detail", args=[self.pk])
        return reverse("dishes:detail_slug", args=[self.pk, self.slug])

    def __str__(self):
        return self.name
