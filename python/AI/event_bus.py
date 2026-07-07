#! /usr/bin/python3

from dataclasses import dataclass
from typing import Any
import heapq
from threading import Lock


@dataclass
class Event:
    timestamp: float
    preference: int = 5  # Max 5
    event_type: str
    payload: Any


class EventBus:
    def __init__(self, maxlen: int = 1000):
        self._queue = []
        self._lock = Lock()
        self._maxlen = maxlen

    def add(self, event: Event):
        item = (-event.preference, event.timestamp, event)
        with self._lock:
            heapq.heappush(self._queue, item)

    def clean(self):
        self._queue = []

    def tic(self):
        element = heapq.heappop(self._queue)
