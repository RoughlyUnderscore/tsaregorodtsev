from abc import ABC, abstractmethod
from typing import Any
from result import Result
from model import EventSession, User


class BookingCommand(ABC):
    def __init__(self):
        self.uninitialized = True
        self._id = -1

    @abstractmethod
    def execute(
        self,
        event: EventSession,
        seat_id: str,
        user: User
    ) -> Result[tuple[Any], str]:
        """
        Выполняет команду. Пользователь не должен вызывать этот метод,
        вместо этого необходимо использовать процессор команд для управления
        исполнением команды.

        Parameters:
            event (EventSession): событие, к которому относится операция
            seat_id: идентификатор места, к которому относится операция
            user: пользователь, выполняющий операцию

        Returns:
            Result: в случае успешного выполнения возращает два списка
            функций - изменения, которые будут выполнены, и отмена изменений.
            В противном случае возвращает строку с информацией об ошибке.
        """
        pass
