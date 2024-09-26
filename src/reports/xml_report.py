from src.abstract.abstract_report import AbstractReport
from src.abstract.format_reporting import FormatReporting
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException
from src.utils.xml_encoder import XmlEncoder


class XmlReport(AbstractReport):
    """
    Отчет формирует набор данных в формате XML
    """

    def __init__(self):
        super().__init__()
        self.__format = FormatReporting.XML

    def create(self, data: list):
        ArgumentException.check_arg(data, list)
        if len(data) == 0:
            raise OperationException("Набор данных пуст!")

        first_model = data[0]
        # список полей
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)),
                             dir(first_model)))
        xmlEncoder = XmlEncoder()
        class_name = type(first_model).__name__
        result = f"<{class_name}>\n"
        for row in data:
            result += "\t<item>\n"
            for field in fields:
                value = getattr(row, field)
                result += "\t\t" + xmlEncoder.default(field, value) + "\n"
            result += "\t</item>\n"
        self._result = f"{result}</{class_name}>\n"
