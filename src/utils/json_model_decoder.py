import importlib
import inspect
import json
import pkgutil
import sys
from json import JSONDecoder

from src.utils.decoders.json_decoder_factory import JsonDecoderFactory


class JsonModelDecoder(JSONDecoder):
    def import_submodules(self, package):
        """Импорт всех подмодулей пакета."""
        module = importlib.import_module(package)
        for loader, name, is_pkg in pkgutil.walk_packages(module.__path__, module.__name__ + '.'):
            importlib.import_module(name)

        return module

    def decode(self, s, _w=...):
        result = super().decode(s, _w)
        return result

    def raw_decode(self, s, idx=0):
        decoded_content: dict = super().raw_decode(s, idx)[0]
        classes = {}
        self.import_submodules("src.models")
        for sub_module in sys.modules:
            if sub_module.startswith("src.models"):
                sub_module_obj = sys.modules[sub_module]
                classes.update({
                    name: cls for name, cls in inspect.getmembers(sub_module_obj, inspect.isclass)
                })
        if "cls" not in decoded_content.keys():
            model_key = list(decoded_content.keys())[0]
        else:
            model_key = decoded_content["cls"]
        cls = [classes[name] for name in classes if name == model_key][0]
        decoder = JsonDecoderFactory().create(cls)
        models = []
        for val in decoded_content[model_key]:
            result = decoder.decode(val)
            models.append(result)
        return models


