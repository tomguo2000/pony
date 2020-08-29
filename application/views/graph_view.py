from .base_view import BaseView
from application.services.graph_service import GraphService
from application.common.foundation import db
from application.services.k_service import KService
import time,json
from application.common.returncode import returncode
from flask import request
import logging



"""
each class is for one API
"""
class GetOnlineView(BaseView):
    def process(self):
        ipaddress = request.args.get('ipaddress')
        action = request.args.get('action','onlineuser',type=str)
        start = request.args.get('start', int(time.time())-36000,type=int)
        end  = request.args.get('end', int(time.time()),type=int)
        logging.info("GetOnlineView. ipaddress:{}. action:{}".format(ipaddress,action))
        if start > end:
            return{
                  "code": 4023,
                  "message": returncode['4023']
            },400

        if action == 'onlineuser':
            data = GraphService.get_online(ipaddress,start,end)
        elif action == 'cpu':
            data = GraphService.get_cpu(ipaddress,start,end)
        elif action == 'network':
            data = GraphService.get_network(ipaddress,start,end)
        else:
            data = []
        return data

class GetKView(BaseView):
    def process(self):
        action = request.args.get('action','user',type=str)
        period =request.args.get('period','hourly',type=str)
        start = request.args.get('start', int(time.time())-86400,type=int)
        end  = request.args.get('end', int(time.time()),type=int)
        logging.info("GetKView. action:{}".format(action))
        if start > end:
            return{
                      "code": 4023,
                      "message": returncode['4023']
                  },400

        if action in ['101','102','103']:
            data = KService.get_user_k(action,period,start,end)
        elif action == '201':
            data = KService.get_order_k(period,start,end)
        else:
            data = ['action parameter error!']
        return data