-- =============================================
-- SQL-запросы проекта «Система учёта заказов кафе»
-- =============================================

-- 1. Список всех блюд (SELECT, ORDER BY)
SELECT id, name, price, category
FROM dishes
ORDER BY name;

-- 2. Поиск блюд по категории (WHERE)
SELECT id, name, price
FROM dishes
WHERE category = 'Напитки'
ORDER BY price;

-- 3. Поиск блюд по максимальной цене (WHERE)
SELECT id, name, price
FROM dishes
WHERE price <= 200
ORDER BY price DESC;

-- 4. Список сотрудников (SELECT)
SELECT id, name, position
FROM employees
ORDER BY name;

-- 5. Заказы с именами сотрудников (JOIN)
SELECT orders.id, orders.order_date, orders.status, employees.name AS employee_name
FROM orders
JOIN employees ON orders.employee_id = employees.id
ORDER BY orders.order_date DESC;

-- 6. Полная информация о заказе (JOIN двух таблиц)
SELECT 
    orders.id AS order_id,
    orders.order_date,
    employees.name AS employee_name,
    dishes.name AS dish_name,
    order_items.quantity,
    (dishes.price * order_items.quantity) AS total_price
FROM orders
JOIN employees ON orders.employee_id = employees.id
JOIN order_items ON orders.id = order_items.order_id
JOIN dishes ON order_items.dish_id = dishes.id
WHERE orders.id = 1;

-- 7. Общее количество заказов (COUNT)
SELECT COUNT(*) AS total_orders
FROM orders;

-- 8. Средняя цена блюда (AVG)
SELECT AVG(price) AS average_price
FROM dishes;

-- 9. Количество заказов по статусам (GROUP BY)
SELECT status, COUNT(*) AS orders_count
FROM orders
GROUP BY status;

-- 10. Выручка по каждому заказу (GROUP BY + JOIN)
SELECT 
    orders.id AS order_id,
    orders.order_date,
    SUM(dishes.price * order_items.quantity) AS order_total
FROM orders
JOIN order_items ON orders.id = order_items.order_id
JOIN dishes ON order_items.dish_id = dishes.id
GROUP BY orders.id, orders.order_date
ORDER BY order_total DESC;

-- 11. Самые популярные блюда (GROUP BY + JOIN)
SELECT 
    dishes.name AS dish_name,
    SUM(order_items.quantity) AS total_quantity
FROM order_items
JOIN dishes ON order_items.dish_id = dishes.id
GROUP BY dishes.id, dishes.name
ORDER BY total_quantity DESC;

-- 12. Сотрудники и количество их заказов (LEFT JOIN + GROUP BY)
SELECT 
    employees.name AS employee_name,
    COUNT(orders.id) AS orders_count
FROM employees
LEFT JOIN orders ON employees.id = orders.employee_id
GROUP BY employees.id, employees.name
ORDER BY orders_count DESC;