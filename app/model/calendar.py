from dataclasses import dataclass, field
from datetime import datetime, date, time, timedelta
from typing import ClassVar

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_not_available_error


##------------------------------------------------------------##

@dataclass

class Reminder:

    EMAIL: str = "email"
    SYSTEM: str = "system"

    def __init__(self, date_time: datetime, type: str = EMAIL):
        self.date_time = date_time
        self.type = type

    def __str__(self) -> str:
        return f"Reminder on {self.date_time} of type {self.type}"


@dataclass

class Event:
    
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    reminders: list[Reminder] = field(default_factory = list)
    id: str = field(default_factory = generate_unique_id)

    def add_reminder(self, date_time: datetime, reminder_type: str = Reminder.EMAIL):
        reminder = Reminder(date_time = date_time, type = reminder_type)
        self.reminders.append(reminder)
    
    def delete_reminder(self, reminder_index: int):
        if 0 <= reminder_index < len(self.reminders):
            del self.reminders[reminder_index]
        else:
            reminder_not_found_error()
    
    def __str__(self) -> str:
        return (f"ID: {self.id}\n"
                f"Event title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Time: {self.start_at} - {self.end_at}")
    
class Day:

    def __init__(self, date_: date):
        self.date_ = date_
        self.slots: dict[time, str | None] = {}
        self._init_slots()




