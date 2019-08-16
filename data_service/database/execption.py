from data_service.utils import exception


class UsernameNotFound(exception.Error):
    pass


class UsernameAlreadyExist(exception.Error):
    pass
