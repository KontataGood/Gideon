from collections import defaultdict
from typing import Callable

from gideon.core.event import Event
from gideon.core.event_type import EventType


class EventBus:
    """
    Центральная шина событий Gideon.

    Компоненты могут подписываться на конкретные
    события или на все события системы.
    """

    def __init__(self):
        self._handlers = defaultdict(list)
        self._global_handlers = []

    def subscribe(
        self,
        event_type: EventType,
        handler: Callable[[Event], None],
    ):
        """Подписывает обработчик на конкретный тип события."""

        self._handlers[event_type].append(handler)

    def subscribe_all(
        self,
        handler: Callable[[Event], None],
    ):
        """Подписывает обработчик на все события."""

        self._global_handlers.append(handler)

    def publish(self, event: Event):
        """Публикует событие."""

        for handler in self._handlers[event.type]:
            handler(event)

        for handler in self._global_handlers:
            handler(event)