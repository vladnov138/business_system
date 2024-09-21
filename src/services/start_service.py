from src.data.data_repository import DataRepository
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.settings_model import Settings
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
        recipes = recipe_manager.convert(self.__repository.data[DataRepository.measurement_unit_key()])
        self.__repository.data[DataRepository.recipe_key()] = recipes


    def create(self):
        """
        Первый старт
        """
        self.__create_nomenclature_groups()
        self.__create_measurement_units()
        self.__create_nomenclature()
        self.__create_recipe()
