from typing import List
import glob
import os


class Error(Exception):
    pass


class WrongNumberOfKeysError(Error):
    def __init__(self, message):
        self.message = message


class WrongParameterTypeError(Error):
    def __init__(self, key, is_type, should_be_type):
        self.message = f"Argument {key} is of type {is_type}, expected type: {should_be_type}"


class FileHandler:
    @staticmethod
    def find_excel_files(directory: str) -> List[str]:
        return glob.glob(f"{directory}\\*.xlsx")

    @staticmethod
    def clear_directory(directory: str) -> None:
        files = glob.glob(f"{directory}\\*.xlsx")
        for file in files:
            os.remove(file)


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))
