from src.abstract.abstract_logic import AbstractLogic
from src.core.event_type import EventType
from src.data.data_repository import DataRepository
from src.exceptions.argument_exception import ArgumentException
from src.models.nomenclature_model import NomenclatureModel


class TurnoverService(AbstractLogic):
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: EventType, **kwargs):
        super().handle_event(type, **kwargs)
        if type != EventType.CHANGE_NOMENCLATURE:
            return
        try:
            ArgumentException.check_arg(kwargs.get("nomenclature"), NomenclatureModel)
            ArgumentException.check_arg(kwargs.get("data"), DataRepository)
        except Exception as e:
            raise ArgumentException("Invalid arguments in kwargs") from e
        nomenclature = kwargs["nomenclature"]
        repository: DataRepository = kwargs["data"]
        turnover_key = repository.turnovers_key()
        turnovers = repository.data[turnover_key]
        match(type):
            case EventType.CHANGE_NOMENCLATURE:
                for turnover in turnovers:
                    if nomenclature.uid == turnover.nomenclature.uid:
                        turnover.nomenclature = nomenclature
                        turnovers[turnovers.index(turnover)] = turnover
                        break
        repository.data[turnover_key] = turnovers

