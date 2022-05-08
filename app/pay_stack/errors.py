
class PyPickrErrors(Exception):
    """
    Python Pickr Error
    """
    pass

class MissingAuthKeyError(PyPickrErrors):
    """
    We can't find the authentication key
    """
    pass


class InvalidMethodError(PyPickrErrors):
    """
    Invalid or unrecoginised/unimplemented HTTP request method
    """
    pass


class InvalidDataError(PyPickrErrors):
    """
    Invalid input recognised. Saves unecessary trip to server
    """
    pass

