from .base_service import BaseService
from application.models.order_model import OrderModel
from application.common.foundation import db
from application.models.route_model import CpuIOModel,DiskIOModel,NetworkModel,LoadAverageModel,OnlineUserAmountModel
from sqlalchemy import between,desc
MAXLIST = 2000

class GraphService(BaseService):

    @staticmethod
    def ToAddtime(data,tomem = False):
        import time
        #格式化addtime列
        if tomem:
            import psutil
            mPre = (psutil.virtual_memory().total / 1024 / 1024) / 100
        length = len(data)
        for i in range(length):
            data[i]['addtime'] = time.strftime('%m/%d %H:%M',time.localtime(float(data[i]['addtime'])))
            if tomem and data[i]['mem'] > 100: data[i]['mem'] = data[i]['mem'] / mPre
        return data



    @staticmethod
    def get_online(ipaddress,start,end):
        amount = OnlineUserAmountModel.query \
            .filter(OnlineUserAmountModel.ipaddress == ipaddress) \
            .filter(between(OnlineUserAmountModel.addtime,start,end)) \
            .count()

        n = int(amount/MAXLIST)

        list = OnlineUserAmountModel.query \
            .filter(OnlineUserAmountModel.ipaddress == ipaddress) \
            .filter(between(OnlineUserAmountModel.addtime,start,end)) \
            .filter(OnlineUserAmountModel.id %n == 0) \
            .all()

        data =[]
        for row in list:
            data.append({'online_user_amount':row.online_user_amount,'server_local_time':row.server_local_time,'addtime':row.addtime})

        print (len(data))
        return GraphService.ToAddtime(data)


    @staticmethod
    def get_cpu(ipaddress,start,end):
        list = CpuIOModel.query \
            .filter(CpuIOModel.ipaddress == ipaddress) \
            .filter(between(CpuIOModel.addtime,start,end)).all()
        data =[]
        for row in list:
            data.append({'cpu':row.cpu,'id':row.id,'addtime':row.addtime})
        return GraphService.ToAddtime(data)


    @staticmethod
    def get_network(ipaddress,start,end):
        import pymysql.cursors
        connection = pymysql.connect(host='114.115.144.166',
                                     user='pony',
                                     password='LCGZFin3w2zGwTjH',
                                     db='pony',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql0 = "SELECT count(1) FROM `network` WHERE `ipaddress`='{}' and `addtime` > {} and `addtime` < {}".format(ipaddress,start,end,)
                cursor.execute(sql0)
                amount = cursor._rows[0]['count(1)']
                print (amount)
                n=int(amount/MAXLIST)
                sql = "SELECT `up`, `down`, `addtime` FROM `network` WHERE `ipaddress`='{}' \
                and `addtime` > {} and `addtime` < {} and `id` % {} =0".format(ipaddress,start,end,n)
                cursor.execute(sql)
                data = cursor.fetchall()
        finally:
            connection.close()

        # list = NetworkModel.query \
        #     .filter(NetworkModel.ipaddress == ipaddress) \
        #     .filter(between(NetworkModel.addtime,start,end)).all()
        # data =[]
        # for row in list:
        #     data.append({'up':row.up,'down':row.down,'addtime':row.addtime})
        return GraphService.ToAddtime(data)


