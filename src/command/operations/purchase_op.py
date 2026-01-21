from typing import Any
from datetime import datetime
from result import Result, Ok, Err
from command import BookingCommand
from model import EventSession, User, SeatState


class PurchaseTicket(BookingCommand):
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
        if seat.status != SeatState.BOOKED:
            return Err("Это место не забронировано.")
        
        if seat.user is None or seat.user != user:
            return Err("Вы не можете оплатить бронирование данного места.")

        if event.time < datetime.now():
            return Err("Уже нельзя оплатить бронирование на этом событии.")

        def change():
            seat.status = SeatState.SOLD
            seat.user = user
        
        def undo():
            seat.status = SeatState.BOOKED

        staged_changes = [change]
        unstage_changes = [undo]

        return Ok((staged_changes, unstage_changes))
