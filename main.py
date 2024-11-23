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
from src.logger.logger import Logger
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

logger = Logger(manager.settings.log_path, manager.settings.log_level)

# Инициализируем наблюдателя и слушателей
observe_service = ObserveService()
observe_service.append(recipe_manager)
observe_service.append(turnover_service)
observe_service.append(data_manager)
observe_service.append(logger)

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
    ObserveService.raise_event(EventType.LOG_INFO, message="GET /api/reports/formats")
    try:
        arr = []
        format_name = list(filter(lambda x: x, FormatReporting))
        for format in format_name:
            result = {"name": format.name, "value": format.value}
            arr.append(result)
        return arr
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in GET /api/reports/formats")
        raise ex


@app.route("/api/models", methods=["GET"])
def get_models():
    ObserveService.raise_event(EventType.LOG_INFO, message="GET /api/models")
    try:
        return {"models": list(models.keys())}
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in GET /api/models")
        raise ex


@app.route("/api/reports/<model_name>/<format_str>", methods=["GET"])
def reports(model_name: str, format_str: str):
    ObserveService.raise_event(EventType.LOG_INFO, message=f"GET /api/reports/{model_name}/{format_str}")
    try:
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
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in GET /api/reports/{model_name}/{format_str}")
        raise ex


@app.route("/api/filter/<entity>", methods=["POST"])
def filter_model(entity):
    ObserveService.raise_event(EventType.LOG_INFO, message=f"POST /api/filter/{entity}")
    try:
        params = request.get_json()
        ObserveService.raise_event(EventType.LOG_DEBUG, message=f"POST /api/filter/{entity} params: {params}")
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
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in POST /api/filter/{entity}")
        raise ex


@app.route("/api/warehouse_transactions", methods=["POST"])
def warehouse_transactions():
    ObserveService.raise_event(EventType.LOG_INFO, message=f"POST /api/warehouse_transactions")
    try:
        key = repository.warehouse_transaction_key()
        data = repository.data[key]
        params = request.get_json()
        ObserveService.raise_event(EventType.LOG_DEBUG, message=f"POST /api/warehouse_transactions params: {params}")
        filter_items = []
        for param in params:
            filter_item = JsonModelDecoder().decode_model(param, WarehouseFilterItem)
            filter_items.append(filter_item)
        filter_dto = WarehouseTransactionFilterDto.create(filter_items)
        result = FilterService().filter_warehouse_transactions(data, filter_dto)
        return report_service.prepare_report(result)
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in POST /api/warehouse_transactions")
        raise ex


@app.route("/api/warehouse_turnovers", methods=["POST"])
def warehouse_turnovers():
    ObserveService.raise_event(EventType.LOG_INFO, message="POST /api/warehouse_turnovers")
    try:
        key = repository.warehouse_transaction_key()
        data = repository.data[key]
        params = request.get_json()
        ObserveService.raise_event(EventType.LOG_DEBUG, message=f"POST /api/warehouse_turnovers params: {params}")
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
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in POST /api/warehouse_turnovers")
        raise ex


@app.route("/api/date_block", methods=["GET"])
def get_dateblock():
    ObserveService.raise_event(EventType.LOG_INFO, message="GET /api/date_block")
    try:
        return {"dateblock": manager.settings.date_block}
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in GET /api/reports/formats")
        raise ex


@app.route("/api/date_block", methods=["POST"])
def set_dateblock():
    ObserveService.raise_event(EventType.LOG_INFO, message="POST /api/date_block")
    try:
        params = request.get_json()
        ObserveService.raise_event(EventType.LOG_DEBUG, message=f"POST /api/date_block params: {params}")
        date_block = params["dateblock"]
        manager.settings.date_block = date_block
        dateblockUpdater.update(manager.settings.date_block)
        manager.save()
        return get_dateblock()
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in POST /api/date_block")
        raise ex


@app.route("/api/nomenclature/{id}", methods=["GET"])
def get_nomenclature(id: str):
    ObserveService.raise_event(EventType.LOG_INFO, message=f"GET /api/nomenclature/{id}")
    try:
        nomenclature = nomenclature_service.get_nomenclature(id)
        return report_service.prepare_report([nomenclature])
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in GET /api/nomenclature/{id}")
        raise ex


@app.route("/api/nomenclature", methods=["PUT"])
def put_nomenclature():
    ObserveService.raise_event(EventType.LOG_INFO, message="PUT /api/nomenclature")
    try:
        param = request.get_json()
        ObserveService.raise_event(EventType.LOG_DEBUG, message=f"PUT /api/nomenclature params: {param}")
        nomenclature = JsonModelDecoder().decode_model(param, NomenclatureModel)
        nomenclature_service.add_nomenclature(nomenclature)
        return 200
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in PUT /api/nomenclature")
        raise ex


@app.route("/api/nomenclature", methods=["PATCH"])
def patch_nomenclature():
    ObserveService.raise_event(EventType.LOG_INFO, message="PATCH /api/nomenclature")
    try:
        param = request.get_json()
        ObserveService.raise_event(EventType.LOG_DEBUG, message=f"PATCH /api/nomenclature params: {param}")
        nomenclature = JsonModelDecoder().decode_model(param, NomenclatureModel)
        nomenclature_service.update_nomenclature(nomenclature)
        observe_service.raise_event(EventType.CHANGE_NOMENCLATURE, nomenclature=nomenclature, data=repository)
        return 200
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in PATCH /api/nomenclature")
        raise ex


@app.route("/api/nomenclature/{id}", methods=["DELETE"])
def delete_nomenclature(id: str):
    """
    Удаление номенклатуры
    :param id: идентификатор номенклатуры
    :return: кол-во удаленных номенклатур
    """
    ObserveService.raise_event(EventType.LOG_INFO, message=f"DELETE /api/nomenclature/{id}")
    try:
        nomenclature = nomenclature_service.get_nomenclature(id)
        nomenclature_key = repository.nomenclature_key()
        prev_length = len(repository.data[nomenclature_key])
        nomenclature_service.delete_nomenclature(id)
        observe_service.raise_event(EventType.DELETE_NOMENCLATURE, nomenclature=nomenclature, data=repository)
        new_length = len(repository.data[nomenclature_key])
        return prev_length - new_length
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in DELETE /api/nomenclature/{id}")
        raise ex


@app.route("/api/balance_sheet", methods=["GET"])
def get_balance_sheet(start_date: datetime, end_date: datetime, warehouse_id: str):
    ObserveService.raise_event(EventType.LOG_INFO, message="GET /api/balance_sheet")
    try:
        ObserveService.raise_event(EventType.LOG_DEBUG,
                                   message=f"GET /api/balance_sheet header params: start_date: {start_date}, "
                                           f"end_date: {end_date}, warehouse_id: {warehouse_id}")
        process = ProcessFactory().create(ProcessType.BALANCE_SHEET,
                                          start_date=start_date,
                                          end_date=end_date,
                                          warehouse_uid=warehouse_id)
        key = repository.warehouse_transaction_key()
        transactions = repository.data[key]
        result = process.execute(transactions)
        return result
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in GET /api/balance_sheet")
        raise ex

@app.route("/api/save_data", methods=["POST"])
def save_data():
    ObserveService.raise_event(EventType.LOG_INFO, message="POST /api/save_data")
    try:
        param = request.get_json()
        ObserveService.raise_event(EventType.LOG_DEBUG, message=f"POST /api/save_data params: {param}")
        filename = param["filename"]
        manager.settings.generate_data = False
        data_manager.save(filename)
        manager.save()
        observe_service.raise_event(EventType.CHANGE_DATA_GENERATING_SETTING, callback=start.create)
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in POST /api/save_data")
        raise ex

@app.route("/api/load_data", methods=["POST"])
def load_data():
    ObserveService.raise_event(EventType.LOG_INFO, message="POST /api/load_data")
    try:
        param = request.get_json()
        ObserveService.raise_event(EventType.LOG_DEBUG, message=f"POST /api/load_data params: {param}")
        filename = param["filename"]
        data = data_manager.load(filename)
        repository.data = data
    except Exception as ex:
        ObserveService.raise_event(EventType.LOG_ERROR, message=f"{ex} in POST /api/load_data")
        raise ex


if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(host="0.0.0.0", port=8080)
