from .base_view import BaseView
from application.common.foundation import db
from application.services.dashboard_service import DashboardService
import time,json
from application.common.returncode import returncode
from flask import request,make_response,render_template
import logging

class expressorder(BaseView):
    def process(self):
        orderid = request.args.get('orderid',type=str)

        productdetail="12个月金牌会员"
        price="39.99"
        useremail="hahaha@ha.com"
        resp = make_response(render_template('expressorder.html',productdetail=productdetail,price=price,orderid=orderid,useremail=useremail), 200)
        return resp