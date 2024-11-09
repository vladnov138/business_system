from src.abstract.filter_type import FilterType
from src.data.data_repository import DataRepository
from src.dto.filter_dto import FilterDto
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException
from src.logics.filter_item import FilterItem
from src.models.nomenclature_model import NomenclatureModel
from src.services.filter_service import FilterService


class NomenclatureService:
    """
    Класс-сервис для CRUD операций с номенклатурами
    """
    __repository: DataRepository = None
    __nomenclature_key: str = None
    __filter_service: FilterService = None

    def __init__(self, repository: DataRepository, filter_service: FilterService):
        ArgumentException.check_arg(repository, DataRepository)
        ArgumentException.check_arg(filter_service, FilterService)
        self.__repository = repository
        self.__nomenclature_key = repository.nomenclature_key()
        self.__filter_service = filter_service

    def add_nomenclature(self, nomenclature: NomenclatureModel):
        ArgumentException.check_arg(nomenclature, NomenclatureModel)
        nomenclatures = self.__repository.data[self.__nomenclature_key]
        nomenclature_id = nomenclature.uid
        filter_item = FilterItem.create("uid", FilterType.EQUAL, nomenclature_id)
        filter_dto = FilterDto.create([filter_item])
        item = self.__filter_service.filter(nomenclatures, filter_dto)
        if len(item) > 0:
            raise OperationException("Nomenclature already exists!")
        self.__repository.data[self.__nomenclature_key].append(nomenclature)


    def get_nomenclature(self, nomenclature_id: str):
        ArgumentException.check_arg(nomenclature_id, str)
        nomenclatures = self.__repository.data[self.__nomenclature_key]
        filter_item = FilterItem.create("uid", FilterType.EQUAL, nomenclature_id)
        filter_dto = FilterDto.create([filter_item])
        item = self.__filter_service.filter(nomenclatures, filter_dto)
        if len(item) > 0:
            return item[0]
        raise OperationException("Nomenclature not found!")

    def update_nomenclature(self, nomenclature: NomenclatureModel):
        ArgumentException.check_arg(nomenclature, NomenclatureModel)
        nomenclatures = self.__repository.data[self.__nomenclature_key]
        nomenclature_id = nomenclature.uid
        filter_item = FilterItem.create("uid", FilterType.EQUAL, nomenclature_id)
        filter_dto = FilterDto.create([filter_item])
        item = self.__filter_service.filter(nomenclatures, filter_dto)
        if len(item) == 0:
            raise OperationException("Nomenclature not found!")
        nomenclatures[nomenclatures.index(item[0])] = nomenclature
        self.__repository.data[self.__nomenclature_key] = nomenclatures

    def delete_nomenclature(self, nomenclature_id: str):
        ArgumentException.check_arg(nomenclature_id, str)
        nomenclatures = self.__repository.data[self.__nomenclature_key]
        filter_item = FilterItem.create("uid", FilterType.EQUAL, nomenclature_id)
        filter_dto = FilterDto.create([filter_item])
        item = self.__filter_service.filter(nomenclatures, filter_dto)
        if len(item) == 0:
            raise OperationException("Nomenclature not found!")
        nomenclatures.remove(item[0])
        self.__repository.data[self.__nomenclature_key] = nomenclatures