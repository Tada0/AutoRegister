from src.common import FileHandler
from typing import Tuple, List
import pandas
import numpy
import os


class XLSXHandler:

    REQUIRED_COLUMNS = (
        'name',
        'surname',
        'email',
        'password',
        'phone number'
    )

    @staticmethod
    def read_xlsx(filename: str) -> pandas.DataFrame:
        try:
            return pandas.read_excel(filename, sheet_name='Sheet1', dtype='str')
        except FileNotFoundError as error:
            print(f"{error}\nThat excel file does not exist!")
            os._exit(1)

    @staticmethod
    def validate_files(directory: str) -> Tuple[List[str], List[str]]:
        xlsx_files = FileHandler.find_excel_files(directory)
        valid_files = [
            file for file in xlsx_files if set(XLSXHandler.read_xlsx(file).keys()) == set(XLSXHandler.REQUIRED_COLUMNS)
        ]
        return valid_files, list(set(xlsx_files) - set(valid_files))

    @staticmethod
    def fetch_new_users(valid_files: List[str]) -> Tuple[Tuple[Tuple[str]], Tuple[Tuple[str]]]:
        all_users = numpy.concatenate([XLSXHandler.read_xlsx(file) for file in valid_files]).tolist()
        valid_users = [user for user in all_users if all(type(data) == str for data in user) and len(user) == 5]
        return [dict(zip(XLSXHandler.REQUIRED_COLUMNS, user)) for user in valid_users], \
               [dict(zip(XLSXHandler.REQUIRED_COLUMNS, user)) for user in all_users if user not in valid_users]

    @staticmethod
    def filter_empty_rows(data_frame: List) -> List:
        return [row for row in data_frame if not all(type(data) == float for data in row.values())]
