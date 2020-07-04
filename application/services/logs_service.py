from .base_service import BaseService
from application.models.logs_model import LogsModel
from application.common.foundation import db
import time
from flask import request

class LogsService(BaseService):
    @staticmethod
    def logging(message,userID):
        timeStamp=time.time()
        localTime = time.localtime(timeStamp)
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)

        logdata = LogsModel(
            logtime = strTime,
            content = message,
            user_id = userID,
            remote_ip = request.remote_addr
        )

        db.session.add(logdata)
        db.session.commit()



