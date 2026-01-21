"""
Вам необходимо реализовать систему бронирования мест на мероприятие (Event).
Система поддерживает операции:
- ReserveSeat (бронирование)
- CancelReservation (отмена)
- PurchaseTicket (подтверждение брони и оплата)
- ChangeSeat

Каждая операция должна:
- Иметь метод execute(EventSession session, String seatId, User user).
- Менять состояние сеанса и конкретного места (статус: свободно, забронировано, продано).
- Могла быть отменена (undo).
Все изменения должны происходить только через эти операции.

Ключевые сущности:
- EventSession (id, time, map of seats).
- Seat (id, row, number, status, currentUser).
- User (id, name).
- BookingCommand (интерфейс команды).
- BookingProcessor, обеспечивающий последовательность и атомарность операций.

Реализуйте систему с привязкой к пользователям и сеансам мероприятия. В качестве ответа: ссылка на репозиторий с решением.
"""

from model import User, Seat, EventSession
from datetime import datetime
from command import BookingProcessor
from command.operations import CancelReservation, ChangeSeat, PurchaseTicket, ReserveSeat

event = EventSession(
    id="Дебют ИРИТ-РТФ",
    time=datetime(2026, 1, 30, 16, 30, 0),
    seats={
        "A1": Seat("A1", 1, 1),
        "A2": Seat("A2", 1, 2),
        "A3": Seat("A3", 1, 3),
        "A4": Seat("A4", 1, 4),
        "B1": Seat("B1", 2, 1),
        "B2": Seat("B2", 2, 2),
        "B3": Seat("B3", 2, 3),
        "B4": Seat("B4", 2, 4),
    }
)

better = User("ГП", "Георгий Палыч")
worse = User("ИН", "Илья Николаич")
mid = User("ВА", "Виктор Анатолич")

proc = BookingProcessor()

# Бронирование места
reserve_id = proc.execute(event, "A3", better, ReserveSeat())
print(event.seats["A3"])

# Попытка забронировать место, которое уже было забронировано
try:
    proc.execute(event, "A3", worse, ReserveSeat())
except RuntimeError as ex:
    print("Не удалось выполнить операцию. Причина:", ex)

# Откат операции
proc.rollback(reserve_id)
print(event.seats["A3"])

# Теперь Илья Николаич может отжать место...
proc.execute(event, "A3", worse, ReserveSeat())
print(event.seats["A3"])

# Отмена бронирования (Георгий Палыч пытается отменить бронь Ильи Николаича)
try:
    proc.execute(event, "A3", better, CancelReservation())
except RuntimeError as ex:
    print("Не удалось выполнить операцию. Причина:", ex)

# Илья Николаич отменяет бронирование собственноручно
cancel_id = proc.execute(event, "A3", worse, CancelReservation())
print(event.seats["A3"])

# Георгий Палыч бронирует место...
rival_reserve_id = proc.execute(event, "A3", better, ReserveSeat())

# А Илья Николаич после этого пытается откатить отмену своей брони.
# Но у него ничего не получится.
try:
    proc.rollback(cancel_id)
except RuntimeError as ex:
    print("Не удалось выполнить операцию. Причина:", ex)

# Но если Георгий Палыч откатит бронь, то Илья Николаич сможет откатить свою отмену
proc.rollback(rival_reserve_id)
proc.rollback(cancel_id)
print(event.seats["A3"])

# Георгий Палыч хочет купить место по соседству
try:
    proc.execute(event, "A2", better, PurchaseTicket())
except RuntimeError as ex:
    print("Не удалось выполнить операцию. Причина:", ex)

# Но он совсем забыл его забронировать! Он исправляет свою ошибку
proc.execute(event, "A2", better, ReserveSeat())
proc.execute(event, "A2", better, PurchaseTicket())

print(event.seats["A2"])
print(event.seats["A3"])

# Илья Николаич перемещается на другое место
change_id = proc.execute(event, "A4", worse, ChangeSeat())
print(event.seats["A3"])
print(event.seats["A4"])

# А потом вообще отменяет бронь... (причем сначала путает место)
try:
    proc.execute(event, "A3", worse, CancelReservation())
except RuntimeError as ex:
    print("Не удалось выполнить операцию. Причина:", ex)
proc.execute(event, "A4", worse, CancelReservation())

# А затем одумывается и пытается отменить смену места, но вот беда,
# место можно сменить только в том случае, если ты забронировал другое,
# иначе что на что менять?
try:
    proc.rollback(change_id)
except RuntimeError as ex:
    print("Не удалось выполнить операцию. Причина:", ex)

# По какой-то причине Илья Николаич бронирует вообще рандомное место,
# в то время как Виктор Анатолич бронирует место A3
proc.execute(event, "B1", worse, ReserveSeat())
proc.execute(event, "A3", mid, ReserveSeat())

# Илья Николаич вспоминает, что у него есть операция отката (откатить бронь
# нынешнего места и вернуть бронь места A3), но откат нельзя произвести,
# ведь место A3 уже занято...
try:
    proc.rollback(change_id)
except RuntimeError as ex:
    print("Не удалось выполнить операцию. Причина:", ex)

# Вроде вся демонстрация функционала.
for seat in event.seats.values():
    print(seat)