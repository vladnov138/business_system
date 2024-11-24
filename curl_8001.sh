#!/bin/bash


# Изменить дату блокировки
curl -X POST "http://localhost:8001/api/date_block" \
  -H "Content-Type: application/json" \
  -d '{
    "dateblock": "2024-12-31"
  }'

# Получить uid единицы измерения и группы
measurement_unit_uid=$(curl -s -X GET "http://localhost:8001/api/reports/MeasurementUnitModel/3" -H "Accept: application/json" | jq -r '.MeasurementUnitModel[0].uid')
group_uid=$(curl -s -X GET "http://localhost:8001/api/reports/NomenclatureGroupModel/3" -H "Accept: application/json" | jq -r '.NomenclatureGroupModel[0].uid')

# Добавить новую номенклатуру
curl -X PUT "http://localhost:8001/api/nomenclature" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"New Item\",
    \"nomenclature_group\": {
      \"uid\": \"$group_uid\",
      \"name\": \"Test Group\"
    },
    \"measurement_unit\": {
      \"uid\": \"$measurement_unit\",
      \"name\": \"kg\"
    }
  }"
