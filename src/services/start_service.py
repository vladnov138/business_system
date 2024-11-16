from datetime import datetime

from src.abstract.date_filter_type import DateFilterType
from src.abstract.period_filter_item import PeriodFilterItem
from src.abstract.process_type import ProcessType
from src.data.data_repository import DataRepository
from src.dto.warehouse_transaction_filter_dto import WarehouseTransactionFilterDto
from src.logics.warehouse_filter_item import WarehouseFilterItem
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.settings_model import Settings
from src.models.warehouse_model import WarehouseModel
from src.models.warehouse_transaction_model import WarehouseTransactionModel
from src.processes.process_factory import ProcessFactory
from src.services.filter_service import FilterService
from src.services.measurement_unit_manager import MeasurementUnitManager
from src.services.recipe_manager import RecipeManager


class StartService:
    __repository: DataRepository = None
    __settings: Settings = None

    def __init__(self, repository: DataRepository, settings: Settings):
        super().__init__()
        self.__repository = repository
        self.__settings = settings

    def __create_nomenclature_groups(self):
        """
        Формирует экземпляры класса группы номенклатур
        :return:
        """
        list = [NomenclatureGroupModel.default_group_cold(), NomenclatureGroupModel.default_group_source()]
        self.__repository.data[DataRepository.group_key()] = list

    def __create_measurement_units(self):
        """
        Формирует экземпляры класса единиц измерения
        :return:
        """
        MeasurementUnitManager().open(self.__settings.measurement_units_path)
        units = MeasurementUnitManager().convert()
        self.__repository.data[DataRepository.measurement_unit_key()] = units

    def __create_nomenclature(self):
        """
        Формирует экземпляры класса номенклатуры
        Для формирования необходимо сперва уже сформировать единицы измерения и группы номенклатур
        :return:
        """
        groups_list = self.__repository.data[DataRepository.group_key()]
        measurements = self.__repository.data[DataRepository.measurement_unit_key()]
        nomenclatures = [NomenclatureModel.default_flour_nomenclature(groups_list[1], measurements[1]),
                         NomenclatureModel.default_ice_nomenclature(groups_list[0], measurements[0])]
        self.__repository.data[DataRepository.nomenclature_key()] = nomenclatures

    def __create_recipe(self):
        """
        Формирует экземпляры класса рецепты
        Для формирования необходимо сперва уже сформировать единицы измерения
        :return:
        """
        recipe_manager = RecipeManager()
        recipe_manager.open(self.__settings.recipe_folder)
        recipes = recipe_manager.convert(self.__repository.data[DataRepository.measurement_unit_key()], self.__repository)
        self.__repository.data[DataRepository.recipe_key()] = recipes

    def __create_warehouse(self):
        """
        Формирует экземпляр класса склада
        :return:
        """
        warehouse = WarehouseModel.default_warehouse()
        self.__repository.data[DataRepository.warehouse_key()] = [warehouse]

    def __create_warehouse_transactions(self):
        """
        Формирует экземпляры класса транзакции склада
        Для формирования необходимо уже сформировать номенклатуры и единицы измерения
        :return:
        """
        warehouse = self.__repository.data[DataRepository.warehouse_key()][0]
        nomenclatures = self.__repository.data[DataRepository.nomenclature_key()]
        nomenclature = nomenclatures[0]
        measurement_unit = self.__repository.data[DataRepository.measurement_unit_key()][0]
        income_transaction1 = WarehouseTransactionModel.default_income_transaction(warehouse, nomenclature,
                                                                                   measurement_unit)
        income_transaction2 = WarehouseTransactionModel.default_income_transaction(warehouse, nomenclature,
                                                                                   measurement_unit,
                                                                                   datetime(2024, 1, 1))
        expense_transaction = WarehouseTransactionModel.default_expense_transaction(warehouse, nomenclature,
                                                                                    measurement_unit)
        self.__repository.data[DataRepository.warehouse_transaction_key()] = [income_transaction1, expense_transaction,
                                                                              income_transaction2]

    def __create_turnovers(self):
        """
        Формирует экземпляры класса оборотов
        Для формирования необходима дата блокировки (настройки) и уже сформированные транзакции
        :return:
        """
        filter_item_after = WarehouseFilterItem()
        before_dateblock_filter_item = PeriodFilterItem()
        before_dateblock_filter_item.date = datetime(1900, 1, 1)
        before_dateblock_filter_item.filter_type = DateFilterType.AFTER
        filter_item_after.period = before_dateblock_filter_item
        filter_item_before = WarehouseFilterItem()
        dateblock_filter_item = PeriodFilterItem()
        dateblock_filter_item.date = self.__settings.date_block
        dateblock_filter_item.filter_type = DateFilterType.BEFORE
        filter_item_before.period = dateblock_filter_item
        filter_dto = WarehouseTransactionFilterDto.create([filter_item_after, filter_item_before])

        transaction_key = self.__repository.warehouse_transaction_key()
        transactions = self.__repository.data[transaction_key]
        filtered_transactions = FilterService().filter_warehouse_transactions(transactions, filter_dto)

        process = ProcessFactory().create(ProcessType.TURNOVER)
        turnovers = process.execute(filtered_transactions)

        turnovers_key = self.__repository.turnovers_key()
        self.__repository.data[turnovers_key] = turnovers

    def create(self):
        """
        Первый старт
        """
        if self.__settings.generate_data:
            self.__create_nomenclature_groups()
            self.__create_measurement_units()
            self.__create_nomenclature()
            self.__create_recipe()
            self.__create_warehouse()
            self.__create_warehouse_transactions()
            self.__create_turnovers()
