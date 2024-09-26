import xml.etree.ElementTree as ET
from xml.dom import minidom


class XmlEncoder:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(XmlEncoder, cls).__new__(cls)
        return cls.instance

    def __default(self, parent: ET.Element, node_name: str, o: object):
        if hasattr(o, '__dict__'):
            return self.__cvt_dict_obj(parent, node_name, o)
        return self.__cvt_default_obj(parent, node_name, o)

    def dump_data(self, data: list):
        first_model = data[0]
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)),
                             dir(first_model)))
        class_name = type(first_model).__name__
        result = ET.Element(class_name)
        for row in data:
            item = ET.SubElement(result, "item")
            for field in fields:
                value = getattr(row, field)
                self.__default(item, field, value)
        str_result = ET.tostring(result, encoding='utf-8')
        reparsed = minidom.parseString(str_result)
        pretty_xml_as_string = reparsed.toprettyxml(indent="  ")
        return pretty_xml_as_string

    def __cvt_dict_obj(self, parent: ET.Element, node_name: str, o: object):
        child = ET.SubElement(parent, node_name)
        for k, v in o.__dict__.items():
            key = k.split('__')[-1]
            key = key.lstrip('_')
            self.__default(child, key, v)

    def __cvt_default_obj(self, parent: ET.Element, node_name: str, o: object):
        child = ET.SubElement(parent, node_name)
        child.text = str(o)