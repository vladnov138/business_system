from src.abstract.abstract_logic import AbstractLogic
from src.exceptions.operation_exception import OperationException
from src.models.ingridient_model import IngridientModel
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.utils.decoders.abstract_json_decoder import AbstractJsonDecoder
from src.utils.decoders.ingridient_json_decoder import IngridientJsonDecoder
from src.utils.decoders.measurement_json_decoder import MeasurementJsonDecoder
from src.utils.decoders.nomenclature_group_json_decoder import NomenclatureGroupJsonDecoder
from src.utils.decoders.nomenclature_json_decoder import NomenclatureJsonDecoder


class JsonDecoderFactory(AbstractLogic):
    __decoders = {}

    def __init__(self):
        super().__init__()
        self.__decoders = {
            IngridientModel.__name__: IngridientJsonDecoder,
            MeasurementUnitModel.__name__: MeasurementJsonDecoder,
            NomenclatureModel.__name__: NomenclatureJsonDecoder,
            NomenclatureGroupModel.__name__: NomenclatureGroupJsonDecoder,
        }

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def create(self, cls) -> AbstractJsonDecoder:
        """
        Получить инстанс нужного декодера
        """
        classname = cls.__name__
        if classname not in self.__decoders.keys():
            self.set_exception(OperationException(f"Указанный вариант формата не реализован!"))
        decoder = self.__decoders[classname]
        return decoder(cls)


