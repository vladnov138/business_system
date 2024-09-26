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
        xmlEncoder = XmlEncoder()
        self._result = xmlEncoder.dump_data(data)
