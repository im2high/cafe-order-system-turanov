"""Импорт данных из JSON-файлов в SQLite."""
import json

from db.database import get_connection

DISHES_FILE = "data/dishes.json"
EMPLOYEES_FILE = "data/employees.json"
ORDERS_FILE = "data/orders.json"


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_dishes(conn):
    dishes = load_json(DISHES_FILE)
    conn.executemany(
        """
        INSERT INTO dishes (id, name, price, category)
        VALUES (?, ?, ?, ?)
        """,
        [
            (dish["id"], dish["name"], dish["price"], dish["category"])
            for dish in dishes
        ],
    )


def import_employees(conn):
    employees = load_json(EMPLOYEES_FILE)
    conn.executemany(
        """
        INSERT INTO employees (id, name, position)
        VALUES (?, ?, ?)
        """,
        [
            (emp["id"], emp["name"], emp["position"])
            for emp in employees
        ],
    )


def import_orders(conn):
    orders = load_json(ORDERS_FILE)

    # Сначала импортируем сами заказы
    conn.executemany(
        """
        INSERT INTO orders (id, employee_id, order_date, status)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                order["id"],
                order["employee_id"],
                order["order_date"],
                order["status"],
            )
            for order in orders
        ],
    )

    # Затем — блюда внутри заказов
    items_data = []
    item_id = 1
    for order in orders:
        for item in order.get("items", []):
            items_data.append((
                item_id,
                order["id"],
                item["dish_id"],
                item["quantity"],
            ))
            item_id += 1

    conn.executemany(
        """
        INSERT INTO order_items (id, order_id, dish_id, quantity)
        VALUES (?, ?, ?, ?)
        """,
        items_data,
    )


def main():
    conn = get_connection()
    try:
        import_dishes(conn)
        import_employees(conn)
        import_orders(conn)
        conn.commit()
        print("Импорт завершён.")
    except Exception as error:
        conn.rollback()
        print("Ошибка импорта:", error)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
