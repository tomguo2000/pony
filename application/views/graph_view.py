from .base_view import BaseView
from application.services.graph_service import GraphService
from application.common.foundation import db
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

