from settings.settings_manager import SettingsManager

manager1 = SettingsManager()
manager1.open("./resources/settings.json")
manager1.convert()
print(f"Settings1 - {manager1.settings.business_type}")
