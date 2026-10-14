from datetime import datetime


def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: нужно целое число.")


def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: нужно число.")


def input_date(prompt: str) -> str:
    while True:
        value = input(prompt)
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Ошибка: формат даты ГГГГ-ММ-ДД.")


def input_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value != "":
            return value
        print("Ошибка: строка не должна быть пустой.")
