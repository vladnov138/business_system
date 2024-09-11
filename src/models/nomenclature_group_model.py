from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_model import NomenclatureModel


class NomenclatureGroupModel:
    __nomenclature: NomenclatureModel = None
    __measurement: MeasurementUnitModel = None

    def __init__(self, nomenclature: NomenclatureModel, measurement: MeasurementUnitModel):
        self.__nomenclature = nomenclature
        self.__measurement = measurement