from dataclasses import dataclass
from typing import Any

from gideon.core.event_type import EventType


@dataclass(frozen=True)
class Event:
    """
    Событие внутри Gideon.
    """

    type: EventType
    data: dict[str, Any]