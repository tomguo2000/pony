import logging
from flask import request
from application.common.exceptions import UserError
logger = logging.getLogger(__name__)


class BaseView(object):
    def __init__(self, parameters=None):
        self.parameters = parameters
        print(request)
        print(request.remote_addr)
        # print(request.headers)
        # print(request._cached_json)

    def process(self):
        raise NotImplemented()

    def as_view(self):
        try:
            return self.process()

        # add any exceptions here

        except UserError as e:
            return 'User Error', 500
        # the last exception
        except Exception as e:
            logger.exception("Run Time Error", e)
            return 'Run Time Error', 500
