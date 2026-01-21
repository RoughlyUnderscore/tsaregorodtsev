from typing import Any
from datetime import datetime
from result import Result, Ok, Err
from command import BookingCommand
from model import EventSession, User, SeatState


class ChangeSeat(BookingCommand):
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
        
        def get_current():
            return next(
                (
                    seat for seat in event.seats.values()
                    if seat.user == user and seat.status == SeatState.BOOKED
                ),
                None
            )
        
        prev = get_current()
        if not prev:
            return Err("У вас не забронировано не одного места.")

        def change():
            prev.status = SeatState.AVAILABLE
            prev.user = None
            seat.status = SeatState.BOOKED
            seat.user = user
        
        def undo():
            if prev.status != SeatState.AVAILABLE:
                raise RuntimeError("Предыдущее место уже занято или забронировано.")
            
            cur = get_current()
            if not get_current():
                raise RuntimeError("У вас не забронировано ни одного места.")
            
            prev.status = SeatState.BOOKED
            prev.status = user
            seat.status = SeatState.AVAILABLE
            seat.user = None

        staged_changes = [change]
        unstage_changes = [undo]

        return Ok((staged_changes, unstage_changes))
