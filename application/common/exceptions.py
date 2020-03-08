import logging
logger = logging.getLogger(__name__)


class ApiException(Exception):
    def __init__(self, message, ex=None):
        self.ex = ex
        self.message = message
        logger.error("{}.{}".format(message, repr(self.ex)))


class UserError(ApiException):
    pass
