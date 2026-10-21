"""Страницы заказов и статистики через SQLite."""
import sqlite3

from django.shortcuts import render

DB_PATH = "data/cafe.sqlite"


def orders(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    orders_list = conn.execute(
        """
        SELECT
            orders.id,
            orders.order_date,
            orders.status,
            employees.name AS employee_name
        FROM orders
        JOIN employees ON orders.employee_id = employees.id
        ORDER BY orders.order_date DESC
        """
    ).fetchall()
    conn.close()
    return render(request, "orders/order_list.html", {"orders": orders_list})


def order_detail(request, order_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    order = conn.execute(
        """
        SELECT
            orders.id,
            orders.order_date,
            orders.status,
            employees.name AS employee_name
        FROM orders
        JOIN employees ON orders.employee_id = employees.id
        WHERE orders.id = ?
        """,
        [order_id],
    ).fetchone()

    items = []
    if order:
        items = conn.execute(
            """
            SELECT
                dishes.name AS dish_name,
                order_items.quantity,
                dishes.price,
                (dishes.price * order_items.quantity) AS total
            FROM order_items
            JOIN dishes ON order_items.dish_id = dishes.id
            WHERE order_items.order_id = ?
            """,
            [order_id],
        ).fetchall()

    conn.close()

    context = {"order": order, "items": items}
    return render(
        request,
        "orders/order_detail.html",
        context,
        status=404 if order is None else 200,
    )


def statistics(request):
    """Страница статистики по заказам."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Статистика по статусам
    status_stats = conn.execute(
        """
        SELECT status, COUNT(*) AS count
        FROM orders
        GROUP BY status
        """
    ).fetchall()

    # Топ блюд
    top_dishes = conn.execute(
        """
        SELECT
            dishes.name AS dish_name,
            SUM(order_items.quantity) AS total_quantity
        FROM order_items
        JOIN dishes ON order_items.dish_id = dishes.id
        GROUP BY dishes.id, dishes.name
        ORDER BY total_quantity DESC
        """
    ).fetchall()

    conn.close()
    return render(
        request,
        "orders/statistics.html",
        {"status_stats": status_stats, "top_dishes": top_dishes},
    )
