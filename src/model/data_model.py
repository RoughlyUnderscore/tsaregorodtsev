import enum
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """ Модель пользователя, бронирующего/покупающего места. """
    id: str
    name: str


class SeatState(enum.Enum):
    """ Нумерованное состояние места. """
    AVAILABLE = 1
    BOOKED = 0
    SOLD = -1


@dataclass
class Seat:
    """ Модель бронируемого/покупаемого места. """
    id: str
    row: int
    number: int
    status: SeatState = SeatState.AVAILABLE
    user: User | None = None


@dataclass
class EventSession:
    """ Модель события с привязанной датой и местами. """
    id: str
    time: datetime
    seats: dict[str, Seat]
