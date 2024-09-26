import json


class JsonModelEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, '__dict__'):
            result = {}
            for k, v in o.__dict__.items():
                key = k.split('__')[-1]
                key = key.lstrip('_')
                result[key] = v
            return result
        return super().default(o)