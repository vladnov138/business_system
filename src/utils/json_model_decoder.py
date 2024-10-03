import importlib
import inspect
import pkgutil
import sys
from json import JSONDecoder


class JsonModelDecoder(JSONDecoder):
    def __init__(self):
        super().__init__()
        self.classes = {}
        self.import_submodules("src.models")
        for sub_module in sys.modules:
            if sub_module.startswith("src.models"):
                sub_module_obj = sys.modules[sub_module]
                self.classes.update({
                    name: cls for name, cls in inspect.getmembers(sub_module_obj, inspect.isclass)
                })

    def import_submodules(self, package):
        """Импорт всех подмодулей пакета."""
        module = importlib.import_module(package)
        for loader, name, is_pkg in pkgutil.walk_packages(module.__path__, module.__name__ + '.'):
            importlib.import_module(name)
        return module

    def decode_model(self, coded_obj: dict, cls):
        """Декодирование объекта в соответствующую модель."""
        model = cls()  # Создаем инстанс модели
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(model.__class__, x)),
                             dir(model)))

        for field in fields:
            if field not in coded_obj:
                continue

            value = coded_obj[field]
            # Рекурсивно декодируем вложенные объекты
            if isinstance(value, dict):
                field_cls = self.get_field_class(cls, field)
                if field_cls:
                    value = self.decode_model(value, field_cls)

            setattr(model, field, value)

        return model

    def get_field_class(self, cls, field_name):
        """Попытка извлечь тип поля, если оно является объектом модели."""
        annotations = getattr(cls, '__annotations__', {})
        return annotations.get(field_name, None)

    def decode(self, s, _w=...):
        """Основное декодирование JSON-строки."""
        decoded_content: dict = self.raw_decode(s)[0]  # Декодируем в словарь

        if "cls" not in decoded_content.keys():
            model_key = list(decoded_content.keys())[0]
        else:
            model_key = decoded_content["cls"]

        # Поиск соответствующего класса по ключу
        if model_key not in self.classes:
            raise ValueError(f"Класс {model_key} не найден.")

        cls = self.classes[model_key]
        models = []

        for val in decoded_content[model_key]:
            result = self.decode_model(val, cls)  # Декодируем модель
            models.append(result)

        return models
