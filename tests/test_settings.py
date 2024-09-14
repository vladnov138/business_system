import json
import unittest

from src.models.settings_model import Settings
from src.settings.settings_manager import SettingsManager


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()

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

    def test_settings_manager_open_fail(self):
        manager = SettingsManager()
        res = manager.open("randomfilefff")
        assert res == False

    def test_settings_manager_singletone(self):
       manager1 = SettingsManager()
       manager1.open("../settings.json")
       manager2 = SettingsManager()
       assert manager1 == manager2
       assert manager1.settings.inn == manager2.settings.inn
       assert manager1.settings.organization_name == manager2.settings.organization_name


if __name__ == '__main__':
    unittest.main()
