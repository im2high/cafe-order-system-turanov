from datetime import date

ORDER_ID = 101
ORDER_DATE = date(2026, 9, 15)
DISH_NAME = "Капучино"
DISH_PRICE = 180.50
QUANTITY = int("2")
EMPLOYEE_NAME = "Анна"
EMPLOYEE_POSITION = "Официант"
ORDER_STATUS = "cooking"


def calculate_total(price: float, quantity: int) -> float:
    return price * quantity


def get_status_description(status: str) -> str:
    if status == "new":
        return "Новый заказ"
    if status == "cooking":
        return "Готовится"
    if status == "ready":
        return "Готов к выдаче"
    if status == "completed":
        return "Завершен"
    if status == "cancelled":
        return "Отменен"
    return "Неизвестный статус"


def can_cancel_order(status: str) -> bool:
    if status == "new" or status == "cooking":
        return True
    return False


def format_order_info(
    order_id: int,
    order_date: date,
    dish_name: str,
    employee_name: str,
    employee_position: str,
    total: float,
    status: str,
) -> str:
    status_text = get_status_description(status)
    return (
        f"Заказ №{order_id} от {order_date}\n"
        f"Блюдо: {dish_name}\n"
        f"Сотрудник: {employee_name} ({employee_position})\n"
        f"Сумма: {total:.2f} руб.\n"
        f"Статус: {status_text}"
    )


def main() -> None:
    total = calculate_total(DISH_PRICE, QUANTITY)
    info = format_order_info(
        ORDER_ID,
        ORDER_DATE,
        DISH_NAME,
        EMPLOYEE_NAME,
        EMPLOYEE_POSITION,
        total,
        ORDER_STATUS,
    )
    print(info)
    print(f"Можно отменить: {'да' if can_cancel_order(ORDER_STATUS) else 'нет'}")


if __name__ == "__main__":
    main()