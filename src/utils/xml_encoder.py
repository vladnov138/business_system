from xml.etree.ElementTree import XML


class XmlEncoder:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(XmlEncoder, cls).__new__(cls)
        return cls.instance

    def default(self, node: str, o: object):
        if hasattr(o, '__dict__'):
            return self.__cvt_dict_obj(o)
        return self.__cvt_default_obj(node, o)

    def __cvt_dict_obj(self, o):
        result = ""
        for k, v in o.__dict__.items():
            key = k.split('__')[-1]
            key = key.lstrip('_')
            result += f"<{key}>{v}</{key}>"
        return result

    def __cvt_default_obj(self, node, o):
        return f"<{node}>{o}</{node}>"