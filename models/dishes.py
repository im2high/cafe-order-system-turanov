class Dish:
    """Блюдо в меню."""

    def __init__(self, dish_id: int, name: str,
                 price: float, category: str) -> None:
        self.id = dish_id
        self.name = name
        self.price = price
        self.category = category

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} ({self.category}) — {self.price:.2f} руб."


def add_dish(dishes: list[Dish], dish_id: int, name: str,
             price: float, category: str) -> Dish:
    dish = Dish(dish_id, name, price, category)
    dishes.append(dish)
    return dish


def find_dish_by_id(dishes: list[Dish], dish_id: int) -> Dish | None:
    for dish in dishes:
        if dish.id == dish_id:
            return dish
    return None


def find_dishes_by_name(dishes: list[Dish], query: str) -> list[Dish]:
    result = []
    query_lower = query.lower()
    for dish in dishes:
        if query_lower in dish.name.lower():
            result.append(dish)
    return result


def filter_dishes_by_category(dishes: list[Dish], category: str) -> list[Dish]:
    result = []
    for dish in dishes:
        if dish.category == category:
            result.append(dish)
    return result


def sort_dishes_by_price(dishes: list[Dish]) -> list[Dish]:
    return sorted(dishes, key=lambda dish: dish.price)


def show_dishes(dishes: list[Dish]) -> None:
    if len(dishes) == 0:
        print("Список блюд пуст.")
        return
    for dish in dishes:
        print(dish)