from datetime import datetime

import connexion
from flask import request

from src.abstract.format_reporting import FormatReporting
from src.abstract.process_type import ProcessType
from src.core.event_type import EventType
from src.data.data_repository import DataRepository
from src.dto.filter_dto import FilterDto
from src.dto.warehouse_transaction_filter_dto import WarehouseTransactionFilterDto
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException
from src.logics.date_block_updator import DateBlockUpdator
from src.logics.filter_item import FilterItem
from src.logics.warehouse_filter_item import WarehouseFilterItem
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.recipe_model import RecipeModel
from src.models.warehouse_model import WarehouseModel
from src.processes.process_factory import ProcessFactory
from src.services.data_manager import DataManager
from src.services.filter_service import FilterService
from src.services.nomenclature_service import NomenclatureService
from src.services.observe_service import ObserveService
from src.services.recipe_manager import RecipeManager
from src.services.report_service import ReportService
from src.services.settings_manager import SettingsManager
from src.services.start_service import StartService
from src.services.turnover_service import TurnoverService
from src.utils.common import Common
from src.utils.json_model_decoder import JsonModelDecoder

app = connexion.FlaskApp(__name__)
manager = SettingsManager()
manager.open("resources/settings.json")
manager.convert()
repository = DataRepository()
report_service = ReportService()
nomenclature_service = NomenclatureService(repository, FilterService())

recipe_manager = RecipeManager()
turnover_service = TurnoverService()
data_manager = DataManager(repository)


# Инициализируем наблюдателя и слушателей
observe_service = ObserveService()
observe_service.append(recipe_manager)
observe_service.append(turnover_service)
observe_service.append(data_manager)

start = StartService(repository, manager.settings)
start.create()

dateblockUpdater = DateBlockUpdator(manager.settings.date_block, repository, ProcessFactory(), ProcessType.DATEBLOCK)

helper = Common()
models = helper.get_models_dict()

models_keys = {
    NomenclatureModel.__name__: repository.nomenclature_key(),
    MeasurementUnitModel.__name__: repository.measurement_unit_key(),
    RecipeModel.__name__: repository.recipe_key(),
    NomenclatureGroupModel.__name__: repository.group_key(),
    WarehouseModel.__name__: repository.warehouse_key(),
    WarehouseTransactionFilterDto.__name__: repository.warehouse_transaction_key()
}


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
    report = report_service.get_report(repository.data[key], inner_format)
    return report.result


@app.route("/api/filter/<entity>", methods=["POST"])
def filter_model(entity):
    params = request.get_json()
    filter_items = []
    for param in params:
        filter_item = JsonModelDecoder().decode_model(param, FilterItem)
        filter_items.append(filter_item)
    filter_dto = FilterDto.create(filter_items)
    cls = models.get(entity) or None
    if cls is None:
        raise ArgumentException("Invalid model")
    key = models_keys.get(entity) or None
    if key is None:
        raise OperationException("Не существует отчет по этой модели")
    data = repository.data[key]
    filter_service = FilterService()
    result = filter_service.filter(data, filter_dto)
    if len(result) == 0:
        return result
    return report_service.prepare_report(result)


@app.route("/api/warehouse_transactions", methods=["POST"])
def warehouse_transactions():
    key = repository.warehouse_transaction_key()
    data = repository.data[key]
    params = request.get_json()
    filter_items = []
    for param in params:
        filter_item = JsonModelDecoder().decode_model(param, WarehouseFilterItem)
        filter_items.append(filter_item)
    filter_dto = WarehouseTransactionFilterDto.create(filter_items)
    result = FilterService().filter_warehouse_transactions(data, filter_dto)
    return report_service.prepare_report(result)


@app.route("/api/warehouse_turnovers", methods=["POST"])
def warehouse_turnovers():
    key = repository.warehouse_transaction_key()
    data = repository.data[key]
    params = request.get_json()
    filter_items = []
    for param in params:
        filter_item = JsonModelDecoder().decode_model(param, WarehouseFilterItem)
        filter_items.append(filter_item)
    filter_dto = WarehouseTransactionFilterDto.create(filter_items)
    result = FilterService().filter_warehouse_transactions(data, filter_dto)
    turnovers_repository = repository.data[repository.turnovers_key()]
    process = ProcessFactory().create(ProcessType.DATEBLOCK, turnovers=turnovers_repository,
                                        dateblock=manager.settings.date_block)
    turnovers = process.execute(result)
    return report_service.prepare_report(turnovers)


@app.route("/api/date_block", methods=["GET"])
def get_dateblock():
    return {"dateblock": manager.settings.date_block}


@app.route("/api/date_block", methods=["POST"])
def set_dateblock():
    params = request.get_json()
    date_block = params["dateblock"]
    manager.settings.date_block = date_block
    dateblockUpdater.update(manager.settings.date_block)
    manager.save()
    return get_dateblock()

@app.route("/api/nomenclature/{id}", methods=["GET"])
def get_nomenclature(id: str):
    nomenclature = nomenclature_service.get_nomenclature(id)
    return report_service.prepare_report([nomenclature])

@app.route("/api/nomenclature", methods=["PUT"])
def put_nomenclature():
    param = request.get_json()
    nomenclature = JsonModelDecoder().decode_model(param, NomenclatureModel)
    nomenclature_service.add_nomenclature(nomenclature)
    return 200

@app.route("/api/nomenclature", methods=["PATCH"])
def patch_nomenclature():
    param = request.get_json()
    nomenclature = JsonModelDecoder().decode_model(param, NomenclatureModel)
    nomenclature_service.update_nomenclature(nomenclature)
    observe_service.raise_event(EventType.CHANGE_NOMENCLATURE, nomenclature=nomenclature, data=repository)
    return 200

@app.route("/api/nomenclature/{id}", methods=["DELETE"])
def delete_nomenclature(id: str):
    """
    Удаление номенклатуры
    :param id: идентификатор номенклатуры
    :return: кол-во удаленных номенклатур
    """
    nomenclature = nomenclature_service.get_nomenclature(id)
    nomenclature_key = repository.nomenclature_key()
    prev_length = len(repository.data[nomenclature_key])
    nomenclature_service.delete_nomenclature(id)
    observe_service.raise_event(EventType.DELETE_NOMENCLATURE, nomenclature=nomenclature, data=repository)
    new_length = len(repository.data[nomenclature_key])
    return prev_length - new_length

@app.route("/api/balance_sheet", methods=["GET"])
def get_balance_sheet(start_date: datetime, end_date: datetime, warehouse_id: str):
    process = ProcessFactory().create(ProcessType.BALANCE_SHEET,
                                      start_date=start_date,
                                      end_date=end_date,
                                      warehouse_uid=warehouse_id)
    key = repository.warehouse_transaction_key()
    transactions = repository.data[key]
    result = process.execute(transactions)
    return result

@app.route("/api/save_data", methods=["POST"])
def save_data():
    param = request.get_json()
    filename = param["filename"]
    manager.settings.generate_data = False
    data_manager.save(filename)
    manager.save()
    observe_service.raise_event(EventType.CHANGE_DATA_GENERATING_SETTING, callback=start.create)

@app.route("/api/load_data", methods=["POST"])
def load_data():
    param = request.get_json()
    filename = param["filename"]
    data = data_manager.load(filename)
    repository.data = data

if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port=8080)
