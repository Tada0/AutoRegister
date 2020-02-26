class Error(Exception):
    pass


class WrongNumberOfKeysError(Error):
    def __init__(self, message):
        self.message = message


class WrongParameterTypeError(Error):
    def __init__(self, key, is_type, should_be_type):
        self.message = f"Argument {key} is of type {is_type}, expected type: {should_be_type}"
