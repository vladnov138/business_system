from pathlib import Path


class PathUtils:
    @staticmethod
    def get_parent_directory(path, levels_up):
        return Path(path).resolve().parents[levels_up - 1]

    @staticmethod
    def get_files_by_path(path):
        files = []
        for file_path in Path(path).glob("*"):
            if file_path.is_file():
                files.append(file_path)
        return files
