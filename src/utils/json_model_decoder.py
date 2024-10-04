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
        """
        for inheritor in BaseComparingByName.__subclasses__():
            self.classes[inheritor.__name__] = inheritor
        for inheritor in BaseComparingByUid.__subclasses__():
            self.classes[inheritor.__name__] = inheritor

    def decode(self, s, _w=None):
        """
        Основное декодирование JSON-строки
        """
        decoded_content = self.raw_decode(s)[0] if isinstance(s, str) else s
        model_key = self.__get_model_key(decoded_content)
        cls = self.__get_class_by_key(model_key)
        data = decoded_content.get(model_key) or decoded_content[model_key]
        if isinstance(data, list):
            return [self.decode_model(item, cls) for item in data]
        return self.decode_model(data, cls)

    def __get_model_key(self, decoded_content):
        """
        Получает ключ модели, либо 'cls', либо первый ключ в словаре
        """
        model_key = decoded_content.get("cls") or (list(decoded_content.keys())[0] if decoded_content else None)
        if not model_key:
            raise OperationException("Ошибка декодинга: не удалось обнаружить ключ модели.")
        return model_key

    def __get_class_by_key(self, model_key):
        """
        Получает класс по ключу модели
        """
        cls = self.classes.get(model_key)
        if not cls:
            raise OperationException(f"Класс {model_key} не найден среди загруженных моделей.")
        return cls

    def decode_model(self, coded_obj, cls):
        """
        Декодирование объекта в соответствующую модель
        """
        model = cls()
        fields = self.__get_model_fields(model)
        for field in fields:
            if field not in coded_obj:
                continue
            value = coded_obj[field]
            setattr(model, field, self.__decode_field_value(value))
        return model

    def __get_model_fields(self, model):
        """
        Получает все поля модели
        """
        return list(filter(lambda x: not x.startswith("_") and not callable(getattr(model, x)), dir(model)))

    def __decode_field_value(self, value):
        """
        Декодирует значение поля, если это словарь с 'cls', список объектов или обычное значение
        """
        if isinstance(value, dict) and "cls" in value:
            return self.__decode_nested_object(value)
        elif isinstance(value, list):
            return self.__decode_list(value)
        return value

    def __decode_nested_object(self, value):
        """
        Декодирует вложенный объект по ключу cls
        """
        nested_cls_name = value["cls"]
        nested_cls = self.classes.get(nested_cls_name)
        if nested_cls:
            return self.decode_model(value, nested_cls)
        return value

    def __decode_list(self, value):
        """
        Декодирует список объектов, если они содержат 'cls'
        """
        if len(value) > 0 and isinstance(value[0], dict) and "cls" in value[0]:
            nested_cls_name = value[0]["cls"]
            nested_cls = self.classes.get(nested_cls_name)
            if nested_cls:
                return [self.decode_model(item, nested_cls) for item in value]
        return value
