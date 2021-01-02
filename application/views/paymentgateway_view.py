#out_trade_no：EX20210101114240U5P3。trade_no：2021010122001301201402609189。trade_status：TRADE_FINISHED
from .base_view import BaseView
from application.services.order_service import OrderService
from application.services.tracking_service import TrackingService
from application.services.thunderservice_service import GetThunderservice
from application.services.user_service import UserService
from application.services.k_service import KService
from application.common.foundation import db
from application.common.dict import thunder_service_for_expressorderID
import time
from application.common.returncode import returncode
from flask import request,make_response,render_template
import logging




"""
each class is for one API
"""


class FinishOrderView(BaseView):
    def process(self):
        trackinginput = self.parameters.get('body')
        TrackingService.tracking(trackinginput)

        FinishOrderViewbody = self.parameters.get('body')
        order_id    = str(FinishOrderViewbody.get('out_trade_no'))
        paymentSN   = str(FinishOrderViewbody.get('trade_no'))
        paymentTime = str(FinishOrderViewbody.get('timestamp'))
        sign        = str(FinishOrderViewbody.get('sign'))

        if self.check_sign(order_id,paymentSN,paymentTime,sign):

            order = OrderService.get_expressorder(order_id)
            if order:
                if order.thunderserviceStatus == "1":
                    return {
                               "code": 200,
                               "message": "thunder service already fulfilled"
                           },200

                try:
                    OrderService.mark_paid_order(order_id)
                    OrderService.make_fulfill(order_id)
                    return {
                           "code": 200,
                           "message": "thunder service all set"
                    },200
                except:
                    return {
                        "code": 5006,
                        "message": returncode['5006']
                    },401
            else:
                return {
                           "code": 4013,
                           "message": returncode['4013']
                       },401
        else:
            return {
                       "code": 4027,
                       "message": returncode['4027']
                   },401

    def check_sign(self, order_id,paymentSN,paymentTime,sign):

        from config.settings import AK_SK
        import hashlib
        sk = AK_SK['expresspay']['sk']
        sign_oridata = order_id+paymentSN+paymentTime+sk
        sign_oridata = sign_oridata.encode()
        signed = hashlib.md5(sign_oridata).hexdigest()
        if signed == sign.lower():
            return True
        else:
            return False
