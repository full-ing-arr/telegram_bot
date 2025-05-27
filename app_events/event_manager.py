import asyncio
from typing import Type, Callable, Any, TypeVar

class Event:
    pass

T = TypeVar("T", bound=Event)

class EventManager:
    def __init__(self):
        self._listeners: dict[Type[T], list[Callable[[T], Any]]] = {}


    def listen(self, event_type: Type[T], callback: Callable[[T], Any]):
        self._listeners.setdefault(event_type, []).append(callback)

    def clear(self, event_type: Type[T], callback: Callable[[T], Any]):
        if event_type in self._listeners:
            try:
                self._listeners[event_type].remove(callback)
                if not self._listeners[event_type]:
                    del self._listeners[event_type]
            except ValueError:
                pass

    async def invoke(self, event: T):
        for cls in type(event).__mro__:
            if cls in self._listeners:
                for cb in self._listeners[cls]:
                    if asyncio.iscoroutinefunction(cb):
                        await cb(event)
                    else:
                        cb(event)