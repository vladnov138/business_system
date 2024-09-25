import os
from pathlib import Path

from PyRTF.Elements import Document
from PyRTF.Renderer import Renderer
from PyRTF.document.paragraph import Table, Cell, Paragraph
from PyRTF.document.section import Section

from src.abstract.abstract_report import AbstractReport
from src.abstract.format_reporting import FormatReporting
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException
from src.utils.path_utils import PathUtils


class RtfReport(AbstractReport):
    """
    Отчет формирует набор данных в формате RTF
    """
    __document: Document = None

    def __init__(self):
        super().__init__()
        self.__format = FormatReporting.RTF

    def create(self, data: list):
        ArgumentException.check_arg(data, list)
        if len(data) == 0:
            raise OperationException("Набор данных пуст!")

        first_model = data[0]
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)),
                             dir(first_model)))

        doc = Document()
        section = Section()
        doc.Sections.append(section)
        column_widths = [700 * 3] * len(fields)
        table = Table(*column_widths)
        section.append(table)
        header_row = [Cell(Paragraph(field)) for field in fields]
        table.AddRow(*header_row)
        for row_data in data:
            row = [Cell(str(getattr(row_data, field))) for field in fields]
            table.AddRow(*row)
        self._result = str(doc)
        self.__document = doc

    def export(self, path, path_utils: PathUtils = PathUtils()):
        ArgumentException.check_arg(path, str)
        ArgumentException.check_arg(path_utils, PathUtils)
        current_path = Path(__file__).resolve()
        parent_path = path_utils.get_parent_directory(current_path, levels_up=3)
        full_name = os.path.join(parent_path, path)
        Path(str(full_name)).parent.mkdir(parents=True, exist_ok=True)
        with open(full_name, "w", encoding='utf-8') as file:
            renderer = Renderer()
            renderer.Write(self.__document, file)

    @property
    def document(self):
        return self.__document


