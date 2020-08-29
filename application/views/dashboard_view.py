from .base_view import BaseView
from application.common.foundation import db
from application.services.dashboard_service import DashboardService
import time,json
from application.common.returncode import returncode
from flask import request
import logging



"""
each class is for one API
"""
class GetDashboardView(BaseView):
    def process(self):
        action = request.args.get('action','summary',type=str)
        logging.info("GetDashboardView. action:{}".format(action))

        #get 2 sets of timestamp range
        thisDayEnd = int(time.time())
        tempDate = time.localtime(thisDayEnd)
        tempTuple = (tempDate[0],tempDate[1],tempDate[2],0,0,0,0,0,0)
        thisDayStart = int(time.mktime(tempTuple))

        thisMonthEnd = int(time.time())
        tempDate = time.localtime(thisMonthEnd)
        tempTuple = (tempDate[0],tempDate[1],0,0,0,0,0,0,0)
        thisMonthStart = int(time.mktime(tempTuple))

        if action == 'summary':
            data = DashboardService.get_summary(thisDayStart,thisDayEnd,thisMonthStart,thisMonthEnd)
            return {"code":200,"message":"get summary success","results":data}
        elif action == 'serverStatus':
            # DashboardService.get_serverstatus(thisDayStart,thisDayEnd,thisMonthStart,thisMonthEnd)
            # return data
            pass
        elif action == 'groupStatus':
            data = DashboardService.get_allGroupsStatus()
            return {"code":200,"message":"get allGroupsStatus success","results":data}
        else:
            pass
        return {"code": 4024,"message": returncode['4024']},400