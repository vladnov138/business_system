import json
import unittest

from src.models.settings_model import Settings
from src.settings.settings_manager import SettingsManager


"""
Тестирует класс SettingsManager и SettingsModel
"""
class TestSettings(unittest.TestCase):
    """
    Настройка перед каждым тестом
    """
    def setUp(self):
        self.settings = Settings()

    """
    Тестирует загрузку файла и конвертацию данных из него
    """
    def test_file_loading(self):
        settings_manager = SettingsManager()
        file_path = "../resources/test_settings.json"
        with open(file_path) as stream:
            data: dict = json.load(stream)
        settings_manager.open(file_path)
        settings_manager.convert()
        settings_attrs = dir(settings_manager.settings)
        for field in data.keys():
            if field not in settings_attrs:
                self.assertFalse(True)
        self.assertTrue(True)

    """
    Тестирует загрузку файла с несуществующим путем
    """
    def test_settings_manager_open_fail(self):
        manager = SettingsManager()
        res = manager.open("randomfilefff")
        assert res == False

    """
    Тестирование паттерна singletone
    """
    def test_settings_manager_singletone(self):
       manager1 = SettingsManager()
       manager1.open("../settings.json")
       manager2 = SettingsManager()
       assert manager1 == manager2
       assert manager1.settings.inn == manager2.settings.inn
       assert manager1.settings.organization_name == manager2.settings.organization_name


if __name__ == '__main__':
    unittest.main()
