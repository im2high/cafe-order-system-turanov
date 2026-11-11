# Система учёта заказов кафе

## Назначение
Консольное приложение для учёта блюд, сотрудников и заказов в кафе.

## Целевая аудитория
Администраторы и сотрудники кафе.

## Предметная область
Учёт меню и заказов в кафе.

## Основные сущности

### Dish — блюдо
Атрибуты: id, name, price, category.

### Employee — сотрудник
Атрибуты: id, name, position.

### Order — заказ
Атрибуты: id, employee (объект Employee), order_date, status, items.
Методы: add_item(), calculate_total(), cancel(), __str__().

### Status — статус заказа
Константы: NEW, COOKING, READY, COMPLETED, CANCELLED.
Методы: get_description() (@classmethod), can_cancel() (@staticmethod).

## Основные функции
- добавление и поиск блюд;
- добавление и поиск сотрудников;
- создание заказа с добавлением блюд;
- подсчёт суммы заказа;
- отмена заказа;
- фильтрация заказов по статусу;
- статистика по заказам;
- сохранение и загрузка JSON.

## Структура проекта
См. дерево выше.

## Запуск
python main.py

## Тесты
pytest -v

## Проверка качества
flake8 .

## Веб-интерфейс (ПР5)

Django-проект `cafe` с приложениями `homepage`, `dishes`, `employees`, `orders`.

### Страницы

- `/` — главная
- `/dishes/` — список блюд
- `/dishes/<id>/` — карточка блюда
- `/employees/` — список сотрудников
- `/employees/<id>/` — карточка сотрудника
- `/orders/` — список заказов
- `/orders/<id>/` — карточка заказа

### Запуск

python manage.py migrate
python manage.py runserver
# открыть http://127.0.0.1:8000/

## Шаблоны Django (ПР6)

- Базовый шаблон `templates/base.html`.
- Наследование `{% extends %}` + `{% block title %}`, `{% block content %}`.
- Включаемые шаблоны: `includes/navigation.html`, карточки, статус заказа.
- Данные через контекст в `render()`.
- Циклы `{% for %}`, условия `{% if %}`, `{% empty %}`.
- Именованные URL с пространствами имён (`dishes:list`, `orders:detail`).
- Фильтры: `|length`, `|floatformat:2`, `|default:"..."`.
- Статика: `homepage/static/homepage/{css,js,img}/`.
- Функция `page()` удалена, весь веб-интерфейс на `render()`.

## База данных (ПР7)

- SQLite: `data/cafe.sqlite`
- Схема: `sql/schema.sql` (таблицы `dishes`, `employees`, `orders`, `order_items`)
- Импорт из JSON: `db/import_json.py`
- Подключение: `db/database.py` (с `PRAGMA foreign_keys = ON`)
- SQL-запросы: `sql/queries.sql` (12 запросов: SELECT, WHERE, JOIN, агрегаты, GROUP BY)
- Данные из БД используются в Django-представлениях (через `sqlite3.Row`)
- Реализована страница статистики `/orders/statistics/`

## Переход на Django ORM (ПР9)

Веб-страницы используют модели `Dish`, `Employee`, `Order` и `OrderItem`.
Заказ связан с сотрудником, а каждая позиция заказа — с заказом и блюдом.

### Первый запуск после перехода

```bash
python manage.py migrate
python manage.py import_pr7
python manage.py check
python manage.py runserver
```

Команда `import_pr7` читает исходную базу `data/cafe.sqlite` и переносит записи
с их идентификаторами в `db.sqlite3`. Её нужно запускать после миграций, до
добавления новых записей. При повторном запуске уже занятые идентификаторы
пропускаются. Можно передать путь к другой копии старой базы первым аргументом.

На странице блюд есть поиск по названию. На странице заказов есть поиск по
сотруднику или блюду, фильтры по имени сотрудника и статусу, скрытие отменённых
заказов, сортировка и пагинация по 10 заказов. Статистика показывает заказы по
статусам, популярные блюда, среднюю цену блюда и количество заказов сотрудников.

### Пример CRUD в Django shell

Выполни `python manage.py shell` и попробуй операции на временной записи:

```python
from dishes.models import Dish

dish = Dish.objects.create(name="Тестовый чай", price=100, category="Напитки")
dish = Dish.objects.get(pk=dish.pk)
dish.price = 110
dish.save()
dish.delete()
```

## Административная панель и ORM (ПР10)

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Открой `http://127.0.0.1:8000/admin/` и войди под суперпользователем.
В списках блюд, сотрудников и заказов есть поиск и фильтры. Цены блюд
можно менять в списке, а позиции заказа — в карточке заказа.

Миграция блюд заполняет slug для существующих записей. Ссылка из списка
включает ID и slug, а прежняя ссылка `/dishes/<id>/` также работает.
Статусы заказов теперь описаны через `TextChoices`. Значения в базе
остались прежними, поэтому преобразовывать их при миграции не нужно.

На странице `/orders/statistics/` можно посмотреть число активных,
завершённых и отменённых заказов. Выбор даты показывает сотрудников,
у которых нет активных заказов на эту дату. В кафе активными считаются
новые, готовящиеся и готовые к выдаче заказы.

Для проверки SQL останови сервер и запусти его с панелью отладки:

```bash
CAFE_DEBUG_TOOLBAR=1 python manage.py runserver
```

Открой `http://127.0.0.1:8000/orders/` и выбери вкладку SQL в панели.
Проверь запрос подсчёта заказов и запрос получения текущей страницы.
В карточке заказа посмотри, как сотрудник и блюда загружаются через JOIN.

```bash
python manage.py makemigrations --check --dry-run
python manage.py check
python -m pytest -q
```
