import enum
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: str
    name: str


class SeatState(enum.Enum):
    AVAILABLE = 1
    BOOKED = 0
    SOLD = -1


@dataclass
class Seat:
    id: str
    row: int
    number: int
    status: SeatState = SeatState.AVAILABLE
    user: User | None = None


@dataclass
class EventSession:
    id: str
    time: datetime
    seats: dict[str, Seat]
