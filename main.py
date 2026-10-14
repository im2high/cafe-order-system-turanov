"""Точка входа в приложение «Система учёта заказов кафе»."""

from models.dishes import (
    add_dish,
    find_dishes_by_name,
    show_dishes,
    find_dish_by_id,
)
from models.employees import (
    add_employee,
    show_employees,
    find_employee_by_id,
)
from models.orders import (
    create_order,
    cancel_order,
    filter_orders_by_status,
    get_orders_statistics,
    show_orders,
)
from models.statuses import Status
from storage import (
    load_dishes,
    save_dishes,
    load_employees,
    save_employees,
    load_orders,
    save_orders,
)
from utils import input_int, input_float, input_date, input_non_empty


def get_next_id(items: list) -> int:
    """Получить следующий свободный id."""
    max_id = 0
    for item in items:
        if item.id > max_id:
            max_id = item.id
    return max_id + 1


def show_menu() -> None:
    print("\n===== Система учёта заказов кафе =====")
    print("1. Показать блюда")
    print("2. Добавить блюдо")
    print("3. Найти блюдо по названию")
    print("4. Показать сотрудников")
    print("5. Добавить сотрудника")
    print("6. Создать заказ")
    print("7. Показать все заказы")
    print("8. Заказы по статусу")
    print("9. Отменить заказ")
    print("10. Статистика по заказам")
    print("0. Выход")


def create_new_order(orders: list, dishes: list, employees: list) -> None:
    """Диалог создания заказа."""
    if len(dishes) == 0:
        print("Нет блюд. Сначала добавьте блюда.")
        return
    if len(employees) == 0:
        print("Нет сотрудников. Сначала добавьте сотрудника.")
        return

    show_employees(employees)
    employee_id = input_int("ID сотрудника: ")
    employee = find_employee_by_id(employees, employee_id)
    if employee is None:
        print("Сотрудник не найден.")
        return

    order_date = input_date("Дата заказа (ГГГГ-ММ-ДД): ")
    order_id = get_next_id(orders)
    order = create_order(orders, order_id, employee, order_date)

    show_dishes(dishes)
    while True:
        dish_id = input_int("ID блюда (0 — завершить): ")
        if dish_id == 0:
            break
        dish = find_dish_by_id(dishes, dish_id)
        if dish is None:
            print("Блюдо не найдено.")
            continue
        quantity = input_int("Количество: ")
        if quantity <= 0:
            print("Количество должно быть положительным.")
            continue
        order.add_item(dish, quantity)
        print(f"Добавлено: {dish.name} x{quantity}")

    print("\nЗаказ создан:")
    print(order)


def main() -> None:
    """Основной цикл программы."""
    dishes = load_dishes()
    employees = load_employees()
    orders = load_orders(dishes, employees)

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_dishes(dishes)

        elif choice == "2":
            dish_id = get_next_id(dishes)
            name = input_non_empty("Название блюда: ")
            price = input_float("Цена: ")
            category = input_non_empty("Категория: ")
            add_dish(dishes, dish_id, name, price, category)
            print("Блюдо добавлено.")

        elif choice == "3":
            query = input_non_empty("Подстрока названия: ")
            result = find_dishes_by_name(dishes, query)
            show_dishes(result)

        elif choice == "4":
            show_employees(employees)

        elif choice == "5":
            emp_id = get_next_id(employees)
            name = input_non_empty("Имя сотрудника: ")
            position = input_non_empty("Должность: ")
            add_employee(employees, emp_id, name, position)
            print("Сотрудник добавлен.")

        elif choice == "6":
            create_new_order(orders, dishes, employees)

        elif choice == "7":
            show_orders(orders)

        elif choice == "8":
            statuses = ", ".join(Status.DESCRIPTIONS.keys())
            print(f"Доступные статусы: {statuses}")
            status = input_non_empty("Статус: ")
            result = filter_orders_by_status(orders, status)
            show_orders(result)

        elif choice == "9":
            order_id = input_int("ID заказа для отмены: ")
            if cancel_order(orders, order_id):
                print("Заказ отменён.")
            else:
                print("Не удалось отменить " "(не найден или статус не позволяет).")

        elif choice == "10":
            stats = get_orders_statistics(orders)
            print(f"Всего заказов: {stats['total_orders']}")
            print(f"Общая выручка: {stats['total_revenue']:.2f} руб.")
            print("По статусам:")
            for status in stats["by_status"]:
                count = stats["by_status"][status]
                description = Status.get_description(status)
                print(f"  {description}: {count}")

        elif choice == "0":
            save_dishes(dishes)
            save_employees(employees)
            save_orders(orders)
            print("Данные сохранены. До свидания!")
            break

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
