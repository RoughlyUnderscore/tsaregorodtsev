from typing import Any, Dict
from command import BookingCommand
from model import EventSession, User
from result import is_err


class BookingProcessor:
    def __init__(self):
        self.rollbacks: Dict[int, list[Any]] = {}
        self.last = 0
    
    def execute(
        self,
        event: EventSession,
        seat_id: str,
        user: User,
        cmd: BookingCommand
    ) -> int:        
        exec_res = cmd.execute(event, seat_id, user)
        if is_err(exec_res):
            raise RuntimeError(exec_res.err_value)
        
        staged, rollback = exec_res.ok_value
        for change in staged:
            change()
        
        id = self.last
        self.last += 1
        
        self.rollbacks[id] = rollback
        return id
    
    def rollback(self, id: int):
        if id not in self.rollbacks:
            raise RuntimeError("Данная операция не существует," \
            "либо не может быть отменена.")
        
        for rollback in self.rollbacks[id]:
            rollback()