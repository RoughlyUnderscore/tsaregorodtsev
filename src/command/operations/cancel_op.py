from typing import Any
from datetime import datetime
from result import Result, Ok, Err
from command import BookingCommand
from model import EventSession, User, SeatState


class CancelReservation(BookingCommand):
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
            return Err("Вы не можете отменить бронирование данного места.")

        if event.time < datetime.now():
            return Err("Уже нельзя отменить бронирование на этом событии.")

        def change():
            seat.status = SeatState.AVAILABLE
            seat.user = None
        
        def undo():
            if seat.status != SeatState.AVAILABLE:
                raise RuntimeError("Это место уже занято или забронировано.")
            
            seat.status = SeatState.BOOKED
            seat.user = user

        staged_changes = [change]
        unstage_changes = [undo]

        return Ok((staged_changes, unstage_changes))
