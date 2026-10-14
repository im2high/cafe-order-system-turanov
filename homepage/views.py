"""Главная страница и общий HTML-каркас."""
from django.http import HttpResponse


def page(title: str, content: str) -> str:
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{bootstrap}">
</head>
<body>
<nav class="nav container py-2 border-bottom mb-4">
  <a class="nav-link" href="/">Главная</a>
  <a class="nav-link" href="/dishes/">Блюда</a>
  <a class="nav-link" href="/employees/">Сотрудники</a>
  <a class="nav-link" href="/orders/">Заказы</a>
</nav>
<main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница."""
    content = """
    <h1 class="display-4">Система учёта заказов кафе</h1>
    <p class="lead">Консольная версия (ПР3) дополнена веб-интерфейсом (ПР5).</p>
    <p>Основные разделы:</p>
    <a href="/dishes/" class="btn btn-primary me-2">Блюда</a>
    <a href="/employees/" class="btn btn-secondary me-2">Сотрудники</a>
    <a href="/orders/" class="btn btn-success">Заказы</a>
    """
    return HttpResponse(page("Кафе — главная", content))


def page_not_found(request, exception):
    """Страница 404."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )