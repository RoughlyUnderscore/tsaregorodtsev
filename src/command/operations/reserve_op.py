from typing import Any
from datetime import datetime
from result import Result, Ok, Err
from command import BookingCommand
from model import EventSession, User, SeatState


class ReserveSeat(BookingCommand):
    """ Бронирует место для данного пользователя. """

    def __init__(self):
        super().__init__()

    def execute(
        self,
        event: EventSession,
        seat_id: str,
        user: User
    ) -> Result[tuple[Any], str]:
        if seat_id not in event.seats:
            return Err("В данном событии нет такого места.")

        seat = event.seats[seat_id]
        if seat.status != SeatState.AVAILABLE:
            return Err("Это место уже занято.")

        if event.time < datetime.now():
            return Err("На это событие уже нельзя забронировать место.")

        def change():
            seat.status = SeatState.BOOKED
            seat.user = user

        def undo():
            seat.status = SeatState.AVAILABLE
            seat.user = None

        staged_changes = [change]
        unstage_changes = [undo]

        return Ok((staged_changes, unstage_changes))
