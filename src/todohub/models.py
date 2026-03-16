# src/todohub/models.py

from dataclasses import dataclass
from datetime import date
from typing import Literal

Priority = Literal["high", "medium", "low"]


@dataclass
class TodoItem:
    text: str
    project: str
    due: date | None
    priority: Priority | None = None
