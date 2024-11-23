#!/bin/bash

# Получить текущую дату блокировки
curl -X GET "http://localhost:8000/api/date_block" -H "Accept: application/json"

warehouse_uid=$(curl -s -X GET "http://localhost:8001/api/reports/WarehouseModel/3" -H "Accept: application/json" | jq -r '.WarehouseModel[0].uid')

# Получить оборотно-сальдовую ведомость
curl -X GET "http://localhost:8001/api/reports/NomenclatureModel/3" -H "Accept: application/json"