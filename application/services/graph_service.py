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
    def get_data_sqlalchemy(model,ipaddress,columns,start,end):
        amount = model.query \
            .filter(model.ipaddress == ipaddress) \
            .filter(between(model.addtime,start,end)) \
            .count()
        n = int(amount/MAXLIST)
        list = model.query \
            .filter(model.ipaddress == ipaddress) \
            .filter(between(model.addtime,start,end)) \
            .filter(model.id %n == 0) \
            .all()
        data =[]
        for row in list:
            temp = {}
            for column in columns:
                # print (getattr(row,column))
                temp[column] = getattr(row,column)
            data.append(temp)
        return data


    @staticmethod
    def get_data_mysql(table,ipaddress,columns,start,end):
        '''
        import pymysql.cursors
        connection = pymysql.connect(host='114.115.144.166',
                                     user='pony',
                                     password='LCGZFin3w2zGwTjH',
                                     db='pony',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql0 = "SELECT count(1) FROM {} WHERE `ipaddress`='{}' and `addtime` > {} and `addtime` < {}".format(table,ipaddress,start,end,)
                cursor.execute(sql0)
                amount = cursor._rows[0]['count(1)']
                n=int(amount/MAXLIST)
                n = 1 if n == 0 else n
                columns = ','.join(columns)
                sql = "SELECT {} FROM `network` WHERE `ipaddress`='{}' \
                and `addtime` > {} and `addtime` < {} and `id` % {} =0".format(columns,ipaddress,start,end,n)
                cursor.execute(sql)
                data = cursor.fetchall()
                print(data)
        finally:
            connection.close()
        return data
        '''
        sql0 = "SELECT count(1) FROM {} WHERE `ipaddress`='{}' and `addtime` > {} and `addtime` < {}".format(table,ipaddress,start,end,)
        amount = db.session.execute(sql0)
        amount = amount.cursor._rows[0][0]
        n=int(amount/MAXLIST)
        n = 1 if n == 0 else n
        cols = ','.join(columns)
        sql = "SELECT {} FROM {} WHERE `ipaddress`='{}' \
                and `addtime` > {} and `addtime` < {} and `id` % {} =0".format(cols,table,ipaddress,start,end,n)
        list = db.session.execute(sql).fetchall()
        data = []
        for row in list:
            temp = {}
            for column in columns:
                temp[column] = getattr(row,column)
            data.append(temp)
        return data


    @staticmethod
    def get_online(ipaddress,start,end):
        columns = ['online_user_amount','server_local_time','addtime']
        data = GraphService.get_data_sqlalchemy(OnlineUserAmountModel,ipaddress,columns,start,end)
        return GraphService.ToAddtime(data)


    @staticmethod
    def get_cpu(ipaddress,start,end):
        columns = ['cpu','addtime']
        # data = GraphService.get_data_sqlalchemy(CpuIOModel,ipaddress,columns,start,end)
        data = GraphService.get_data_mysql('cpuio',ipaddress,columns,start,end)
        return GraphService.ToAddtime(data)


    @staticmethod
    def get_network(ipaddress,start,end):
        columns = ['up','down','addtime']
        data = GraphService.get_data_mysql('network',ipaddress,columns,start,end)
        # data = GraphService.get_data_sqlalchemy(NetworkModel,ipaddress,columns,start,end)
        return GraphService.ToAddtime(data)


