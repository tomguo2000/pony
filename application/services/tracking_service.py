from .base_service import BaseService
from application.models.tracking_model import TrackingModel
from application.common.foundation import db
import time
from flask import request

class TrackingService(BaseService):
    @staticmethod
    def tracking(input,output,userID):
        timeStamp=time.time()
        localTime = time.localtime(timeStamp)
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)

        trackingdata = TrackingModel(
            logtime = strTime,
            content = input,
            result = output,
            user_id = userID,
            remote_ip = request.remote_addr
        )

        db.session.add(trackingdata)
        db.session.commit()

    @staticmethod
    def search(pageNum,pageSize,userID,content,result):

        list = db.session.query(TrackingModel)

        if userID:
            list = list.filter(TrackingModel.user_id == userID)

        if content:
            list = list.filter(TrackingModel.content.like('%{}%'.format(content)))

        if result:
            list = list.filter(TrackingModel.result == result)


        data=list.limit(pageSize).offset((pageNum-1)*pageSize).all()

        totals = list.count()
        totalPages = (totals + pageSize - 1) // pageSize

        listdata=[]
        for x in data:
            listdata.append({
                "id": x.id,
                "logtime": x.logtime,
                "content": x.content,
                "result":x.result,
                "user_id":x.user_id,
                "remote_ip":x.remote_ip,

            })

        return {
            "code": 200,
            "message": "get users success",
            "results":{
                "totals":totals,
                "totalPages":totalPages,
                "list":listdata
            }
        }


