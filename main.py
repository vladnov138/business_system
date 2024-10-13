import json

import connexion
from flask import request

from src.abstract.abstract_report import AbstractReport
from src.abstract.base_comparing_by_name import BaseComparingByName
from src.abstract.base_comparing_by_uid import BaseComparingByUid
from src.abstract.format_reporting import FormatReporting
from src.data.data_repository import DataRepository
from src.dto.filter_dto import FilterDto
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException
from src.logics.model_prototype import ModelPrototype
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.recipe_model import RecipeModel
from src.reports.report_factory import ReportFactory
from src.services.settings_manager import SettingsManager
from src.services.start_service import StartService
from src.utils.json_model_decoder import JsonModelDecoder

app = connexion.FlaskApp(__name__)
manager = SettingsManager()
manager.open("resources/settings.json")
manager.convert()
repository = DataRepository()
start = StartService(repository, manager.settings)
start.create()

models = {}
for inheritor in BaseComparingByName.__subclasses__():
    models[inheritor.__name__] = inheritor
for inheritor in BaseComparingByUid.__subclasses__():
    models[inheritor.__name__] = inheritor

models_keys = {
    NomenclatureModel.__name__: repository.nomenclature_key(),
    MeasurementUnitModel.__name__: repository.measurement_unit_key(),
    RecipeModel.__name__: repository.recipe_key(),
    NomenclatureGroupModel.__name__: repository.group_key()
}

def get_report(data, format: FormatReporting) -> AbstractReport:
    report = ReportFactory(manager.settings).create(format)
    report.create(data)
    return report

@app.route("/api/reports/formats", methods=["GET"])
def formats():
    format_name = list(filter(lambda x: x, FormatReporting))
    arr = []
    for format in format_name:
        result = {"name": format.name, "value": format.value}
        arr.append(result)
    return arr

@app.route("/api/models", methods=["GET"])
def get_models():
    return {"models": list(models.keys())}

@app.route("/api/reports/<model_name>/<format_str>", methods=["GET"])
def reports(model_name: str, format_str: str):
    if not format_str.isnumeric():
        raise ArgumentException("Format must be is numeric")
    format = int(format_str)
    cls = models.get(model_name) or None
    if cls is None:
        raise ArgumentException("Invalid model")
    key = models_keys.get(model_name) or None
    if key is None:
        raise OperationException("Не существует отчет по этой модели")
    inner_format = FormatReporting(format)
    report = get_report(repository.data[key], inner_format)
    return report.result

@app.route("/api/filter/<entity>", methods=["POST"])
def filter_model(entity):
    filter_dto = JsonModelDecoder().decode_model(request.get_json(), FilterDto)
    cls = models.get(entity) or None
    if cls is None:
        raise ArgumentException("Invalid model")
    key = models_keys.get(entity) or None
    if key is None:
        raise OperationException("Не существует отчет по этой модели")
    data = repository.data[key]
    model_prototype = ModelPrototype(data)
    result = model_prototype.create(data, filter_dto)
    if len(result.data) == 0:
        return result.data
    report_format = FormatReporting(manager.settings.report_format)
    report = ReportFactory(manager.settings).create(report_format)
    report.create(result.data)
    return json.loads(report.result)

if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port=8080)
