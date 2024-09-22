import json
from pathlib import Path


class FileReader:
    @staticmethod
    def read_file(path):
        full_path = Path(path)
        if not full_path.exists():
            raise FileNotFoundError(f"Файл не найден: {full_path}")
        with full_path.open('r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def read_json(path):
        content = FileReader.read_file(path)
        return json.loads(content)