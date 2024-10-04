from json import JSONDecoder

from src.abstract.base_comparing_by_name import BaseComparingByName
from src.abstract.base_comparing_by_uid import BaseComparingByUid
from src.exceptions.operation_exception import OperationException


class JsonModelDecoder(JSONDecoder):

    def __init__(self):
        super().__init__()
        self.classes = {}
        self.import_submodules()

    def import_submodules(self):
        """
        Импорт всех подмодулей пакета
        :return:
        """
        for inheritor in BaseComparingByName.__subclasses__():
            self.classes[inheritor.__name__] = inheritor
        for inheritor in BaseComparingByUid.__subclasses__():
            self.classes[inheritor.__name__] = inheritor

    def decode_model(self, coded_obj, cls):
        """
        Декодирование объекта в соответствующую модель
        :return:
        """
        model = cls()
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(model, x)), dir(model)))

        for field in fields:
            if field not in coded_obj:
                continue
            value = coded_obj[field]

            if isinstance(value, dict) and "cls" in value:
                nested_cls_name = value["cls"]
                nested_cls = self.classes.get(nested_cls_name)
                if nested_cls:
                    value = self.decode_model(value, nested_cls)
            elif isinstance(value, list):
                if len(value) > 0 and isinstance(value[0], dict) and "cls" in value[0]:
                    nested_cls_name = value[0]["cls"]
                    nested_cls = self.classes.get(nested_cls_name)
                    if nested_cls:
                        value = [self.decode_model(item, nested_cls) for item in value]

            setattr(model, field, value)
        return model

    def decode(self, s, _w=None):
        """
        Основное декодирование JSON-строки
        :return:
        """
        if isinstance(s, str):
            decoded_content = self.raw_decode(s)[0]
        else:
            decoded_content = s

        model_key = decoded_content.get("cls") or list(decoded_content.keys())[0]
        if not model_key or model_key not in self.classes:
            raise OperationException("Ошибка декодинга: не удалось обнаружить ключ")

        cls = self.classes.get(model_key)

        if cls is None:
            raise OperationException(f"Класс {model_key} не найден среди загруженных моделей.")

        data = decoded_content.get(model_key) or decoded_content[model_key]
        if isinstance(data, list):
            models = [self.decode_model(item, cls) for item in data]
        else:
            models = self.decode_model(data, cls)

        return models

