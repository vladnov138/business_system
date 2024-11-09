import json
from datetime import datetime
from enum import Enum

class JsonModelEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, Enum):
            return o.name
        elif hasattr(o, '__dict__'):
            result = {"cls": type(o).__name__}
            for k, v in o.__dict__.items():
                if callable(v):
                    continue
                key = k.split('__')[-1].lstrip('_')

                if key == "format_reports" and isinstance(v, dict):
                    result[key] = {enum_key.name: report_class.__module__.split('.')[-1]
                                   for enum_key, report_class in v.items()}
                elif hasattr(v, '__dict__'):
                    result[key] = self.default(v)
                else:
                    if isinstance(v, (str, int, float, bool, type(None))):
                        result[key] = v
                    elif isinstance(v, Enum):
                        result[key] = v.name
                    else:
                        result[key] = str(v)
            return result
        return super().default(o)
