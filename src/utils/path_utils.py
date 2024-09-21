from pathlib import Path


class PathUtils:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PathUtils, cls).__new__(cls)
        return cls.instance

    def get_parent_directory(self, path, levels_up):
        """
        Возвращает родительскую директорию проекта
        :param path: Текущий путь
        :param levels_up: На сколько уровней вверх подняться
        :return: Корень директории проекта
        """
        return Path(path).resolve().parents[levels_up - 1]

    def get_files_by_path(self, path):
        """
        Возвращает все файлы в директории
        :param path: Каталог с файлами
        :return: Список файлов
        """
        files = []
        for file_path in Path(path).glob("*"):
            if file_path.is_file():
                files.append(file_path)
        return files
