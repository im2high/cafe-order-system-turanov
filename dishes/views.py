"""Страницы блюд через SQLite."""
import sqlite3

from django.shortcuts import render

DB_PATH = "data/cafe.sqlite"


def dishes(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    dishes_list = conn.execute(
        "SELECT id, name, price, category FROM dishes ORDER BY name"
    ).fetchall()
    conn.close()
    return render(request, "dishes/dish_list.html", {"dishes": dishes_list})


def dish_detail(request, dish_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    dish = conn.execute(
        "SELECT id, name, price, category FROM dishes WHERE id = ?",
        [dish_id],
    ).fetchone()
    conn.close()
    return render(
        request,
        "dishes/dish_detail.html",
        {"dish": dish},
        status=404 if dish is None else 200,
    )
