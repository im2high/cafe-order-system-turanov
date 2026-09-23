class Status:

    NEW = "new"
    COOKING = "cooking"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    DESCRIPTIONS = {
        NEW: "Новый заказ",
        COOKING: "Готовится",
        READY: "Готов к выдаче",
        COMPLETED: "Завершён",
        CANCELLED: "Отменён",
    }

    @classmethod
    def get_description(cls, status: str) -> str:
        if status in cls.DESCRIPTIONS:
            return cls.DESCRIPTIONS[status]
        return "Неизвестный статус"

    @staticmethod
    def can_cancel(status: str) -> bool:
        if status == Status.NEW:
            return True
        if status == Status.COOKING:
            return True
        return False