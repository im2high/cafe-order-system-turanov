import sqlite3
from contextlib import closing
from datetime import date
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction

from dishes.models import Dish
from employees.models import Employee
from orders.models import Order, OrderItem


class Command(BaseCommand):
    help = "Переносит данные из SQLite ПР7 в модели Django."

    def add_arguments(self, parser):
        parser.add_argument("source", nargs="?", default=settings.BASE_DIR / "data/cafe.sqlite")

    def handle(self, *args, **options):
        source = Path(options["source"]).resolve()
        try:
            with closing(sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)) as old_db:
                with transaction.atomic():
                    self.import_data(old_db)
        except (sqlite3.Error, IntegrityError, ValueError) as error:
            raise CommandError(f"Не удалось перенести данные: {error}") from error

        self.stdout.write(self.style.SUCCESS("Перенос данных из ПР7 завершён."))

    def import_data(self, old_db):
        # Сначала переносим блюда и сотрудников, на которые ссылаются заказы.
        dishes = old_db.execute("SELECT id, name, price, category FROM dishes")
        for pk, name, price, category in dishes:
            Dish.objects.get_or_create(
                pk=pk, defaults={"name": name, "price": Decimal(str(price)), "category": category}
            )

        for pk, name, position in old_db.execute("SELECT id, name, position FROM employees"):
            Employee.objects.get_or_create(pk=pk, defaults={"name": name, "position": position})

        for pk, employee_id, order_date, status in old_db.execute(
            "SELECT id, employee_id, order_date, status FROM orders"
        ):
            Order.objects.get_or_create(
                pk=pk,
                defaults={
                    "employee_id": employee_id,
                    "order_date": date.fromisoformat(order_date),
                    "status": status,
                },
            )

        for pk, order_id, dish_id, quantity in old_db.execute(
            "SELECT id, order_id, dish_id, quantity FROM order_items"
        ):
            OrderItem.objects.get_or_create(
                pk=pk, defaults={"order_id": order_id, "dish_id": dish_id, "quantity": quantity}
            )
