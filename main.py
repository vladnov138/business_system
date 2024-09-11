from src.settings.settings_manager import SettingsManager

manager1 = SettingsManager()
manager1.open("resources/settings.json")
manager1.convert()
print(manager1.settings)
