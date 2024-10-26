import json
from datetime import datetime


class JsonModelEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if hasattr(o, '__dict__'):
            result = {"cls": type(o).__name__}
            for k, v in o.__dict__.items():
                if callable(v):
                    continue
                key = k.split('__')[-1]
                key = key.lstrip('_')
                result[key] = v
            return result
        return super().default(o)