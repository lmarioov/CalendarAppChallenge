from dataclasses import dataclass, field
from datetime import datetime, date, time
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
        self.slots = self._init_slots()
  
    def _init_slots(self):
        slots = {}
        for hour in range(24):
            for minute in range(0, 60, 15):
                time_key = time(hour, minute)
                slots[time_key] = None
        return slots
    
    def add_event(self, event_id: str, start_at: time, end_at: time):
        current_time = start_at
        pass

    def delete_event(self, event_id: str):
        deleted = False

        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot] = None
                deleted = True

        if not deleted:
            event_not_found_error()

    def update_event(self, event_id: str, start_at: time, end_at: time):

        for slot in self.slots:
            if self.slots[slot] == event_id:
                self.slots[slot] = None

        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot]:
                    slot_not_available_error()
                else:
                    self.slots[slot] = event_id


class Calendar:
    def __init__(self):
        self.days: dict[date, Day] = {}
        self.events: dict[str, Event] = {}

    def add_event(self, title: str, description: str, date_: date, start_at: time, end_at: time) -> str:
        if date_ < datetime.now().date():
            date_lower_than_today_error
            

        if date_ not in self.days:
            self.days[date_] = Day(date_)

        event = Event(title = title, description = description, date_ = date_, start_at = start_at, end_at = end_at)
        self.days[date_].add_event(event.id, start_at, end_at)
        self.events[event.id] = event
        
        return event.id
    
    def add_reminder (self, event_id: str, date_time: datetime, type_: str):
        event = self.events.get(event_id)
        if not event:
            event_not_found_error
            

        Event.add_reminder(date_time = date_time, reminder_type = type_)

    