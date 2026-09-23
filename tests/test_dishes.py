from models.dishes import (
    Dish, add_dish, find_dish_by_id,
    find_dishes_by_name, filter_dishes_by_category,
    sort_dishes_by_price,
)


def test_dish_creation():
    dish = Dish(1, "Капучино", 180.5, "Напитки")
    assert dish.id == 1
    assert dish.name == "Капучино"
    assert dish.price == 180.5
    assert dish.category == "Напитки"


def test_dish_str():
    dish = Dish(1, "Капучино", 180.5, "Напитки")
    assert "Капучино" in str(dish)


def test_add_dish():
    dishes = []
    add_dish(dishes, 1, "Капучино", 180.5, "Напитки")
    assert len(dishes) == 1


def test_find_dish_by_id():
    dishes = []
    add_dish(dishes, 1, "Капучино", 180.5, "Напитки")
    assert find_dish_by_id(dishes, 1) is dishes[0]
    assert find_dish_by_id(dishes, 99) is None


def test_find_dishes_by_name():
    dishes = []
    add_dish(dishes, 1, "Капучино", 180.5, "Напитки")
    add_dish(dishes, 2, "Латте", 200.0, "Напитки")
    result = find_dishes_by_name(dishes, "капу")
    assert len(result) == 1


def test_filter_dishes_by_category():
    dishes = []
    add_dish(dishes, 1, "Капучино", 180.5, "Напитки")
    add_dish(dishes, 2, "Круассан", 120.0, "Выпечка")
    result = filter_dishes_by_category(dishes, "Напитки")
    assert len(result) == 1


def test_sort_dishes_by_price():
    dishes = []
    add_dish(dishes, 1, "Капучино", 180.5, "Напитки")
    add_dish(dishes, 2, "Круассан", 120.0, "Выпечка")
    result = sort_dishes_by_price(dishes)
    assert result[0].price == 120.0
    assert result[1].price == 180.5