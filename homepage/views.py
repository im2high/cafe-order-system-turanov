"""Главная страница и обработчик 404."""
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    html = f"""<!DOCTYPE html>
    <html lang="ru"><head><meta charset="UTF-8">
    <title>404 — Кафе</title></head>
    <body><main class="container">{content}</main></body></html>"""
    return HttpResponse(html, status=404)
