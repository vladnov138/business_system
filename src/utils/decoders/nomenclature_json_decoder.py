from src.utils.decoders.abstract_json_decoder import AbstractJsonDecoder


class NomenclatureJsonDecoder(AbstractJsonDecoder):
    def __init__(self, cls):
        super().__init__(cls)

    def decode(self, coded_obj: dict):
        model = self._cls()
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(model.__class__, x)),
                             dir(model)))
        for field in fields:
            if field not in coded_obj:
                continue
            value = coded_obj[field]
            if isinstance(value, dict):
                value = self.decode(value)
            setattr(model, field, value)
        return model