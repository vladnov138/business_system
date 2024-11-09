from src.abstract.abstract_logic import AbstractLogic
from src.core.event_type import EventType
from src.exceptions.argument_exception import ArgumentException


class ObserveService:
    observers = []

    @staticmethod
    def append(service: AbstractLogic):
        if service is None:
            return
        if not isinstance(service, AbstractLogic):
            raise ArgumentException("Некорректный тип данных!")
        items = list(map(lambda x: type(x).__name__, ObserveService.observers))
        found = type( service ).__name__ in items
        if not found:
            ObserveService.observers.append( service )

    @staticmethod
    def raise_event(type: EventType, params):
        for instance in ObserveService.observers:
            if instance is not None:
                instance.handle_event( type, params )