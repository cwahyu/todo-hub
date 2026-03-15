from dataclasses import dataclass
from datetime import date


@dataclass
class TodoItem:
    text: str
    project: str
    due: date | None
