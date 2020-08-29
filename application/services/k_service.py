from .base_service import BaseService
from application.models.k_model import KModel
from application.common.foundation import db
from sqlalchemy import between,desc
import time

class KService(BaseService):

    @staticmethod
    def strfTime(timestamp):
        import time
        re = {}
        re['yearly'] =    time.strftime('%Y',time.localtime(timestamp))
        re['monthly'] =   time.strftime('%Y-%m',time.localtime(timestamp))
        re['daily'] =     time.strftime('%Y-%m-%d',time.localtime(timestamp))
        re['hourly'] =    time.strftime('%Y-%m-%d %H:00',time.localtime(timestamp))
        re['minutely'] =  time.strftime('%Y-%m-%d %H:%M:00',time.localtime(timestamp))
        re['timestamp'] = timestamp
        return re

    @staticmethod
    def add_record(action,parameter1,parameter2,timestamp):
        strfTime = KService.strfTime(timestamp)
        k = KModel()
        k.action=action
        k.parameter1=parameter1
        k.parameter2=parameter2
        for key in strfTime:
            setattr(k,key,strfTime[key])
        db.session.add(k)
        db.session.commit()

    @staticmethod
    def get_user_k(action,period,start,end):
        import datetime
        re = []

        if period == "daily":
            tempstart = time.localtime(start)
            timeTuple = (tempstart[0],tempstart[1],tempstart[2],0,0,0,0,0,0)
            start = int(time.mktime(timeTuple))
            while start < end:
                temp1 = time.strftime('%Y-%m-%d',time.localtime(start))
                temp2 ={"date":temp1,"Windows":0,"iPhone":0,"Android":0,"Mac":0,"Unknown":0}
                re.append(temp2)
                start = datetime.datetime.timestamp(datetime.datetime.fromtimestamp(start)+datetime.timedelta(days=1))
        elif period == "hourly":
            tempstart = time.localtime(start)
            timeTuple = (tempstart[0],tempstart[1],tempstart[2],tempstart[3],0,0,0,0,0)
            start = int(time.mktime(timeTuple))
            while start < end:
                temp1 = time.strftime('%Y-%m-%d %H:00',time.localtime(start))
                temp2 ={"date":temp1,"Windows":0,"iPhone":0,"Android":0,"Mac":0,"Unknown":0}
                re.append(temp2)
                start = datetime.datetime.timestamp(datetime.datetime.fromtimestamp(start)+datetime.timedelta(hours=1))
        elif period == "minutely":
            tempstart = time.localtime(start)
            timeTuple = (tempstart[0],tempstart[1],tempstart[2],tempstart[3],tempstart[4],0,0,0,0)
            start = int(time.mktime(timeTuple))
            while start < end:
                temp1 = time.strftime('%Y-%m-%d %H:%M:00',time.localtime(start))
                temp2 ={"date":temp1,"Windows":0,"iPhone":0,"Android":0,"Mac":0,"Unknown":0}
                re.append(temp2)
                start = datetime.datetime.timestamp(datetime.datetime.fromtimestamp(start)+datetime.timedelta(minutes=1))
        else:
            return ['period parameter error!']

        sql = "SELECT {} as period, parameter2 as device,count(1) as amount from k \
                WHERE action = {} \
                GROUP BY {},parameter2" \
                .format(period,action,period)
        list = db.session.execute(sql).fetchall()
        print (list)
        i =0
        l = len(list)
        if l == 0:
            return re

        for row in re:
            while row['date'] == list[i][0]:
                row[list[i][1]]=list[i][2]
                if i< (l-1):
                    i +=1
                else:
                    break
        return re

    @staticmethod
    def get_order_k(period,start,end):
        import datetime
        re = []

        if period == "daily":
            tempstart = time.localtime(start)
            timeTuple = (tempstart[0],tempstart[1],tempstart[2],0,0,0,0,0,0)
            start = int(time.mktime(timeTuple))
            while start < end:
                temp1 = time.strftime('%Y-%m-%d',time.localtime(start))
                temp2 ={"date":temp1,"New":0,"Paid":0}
                re.append(temp2)
                start = datetime.datetime.timestamp(datetime.datetime.fromtimestamp(start)+datetime.timedelta(days=1))
        elif period == "hourly":
            tempstart = time.localtime(start)
            timeTuple = (tempstart[0],tempstart[1],tempstart[2],tempstart[3],0,0,0,0,0)
            start = int(time.mktime(timeTuple))
            while start < end:
                temp1 = time.strftime('%Y-%m-%d %H:00',time.localtime(start))
                temp2 ={"date":temp1,"New":0,"Paid":0}
                re.append(temp2)
                start = datetime.datetime.timestamp(datetime.datetime.fromtimestamp(start)+datetime.timedelta(hours=1))
        elif period == "minutely":
            tempstart = time.localtime(start)
            timeTuple = (tempstart[0],tempstart[1],tempstart[2],tempstart[3],tempstart[4],0,0,0,0)
            start = int(time.mktime(timeTuple))
            while start < end:
                temp1 = time.strftime('%Y-%m-%d %H:%M:00',time.localtime(start))
                temp2 ={"date":temp1,"New":0,"Paid":0}
                re.append(temp2)
                start = datetime.datetime.timestamp(datetime.datetime.fromtimestamp(start)+datetime.timedelta(minutes=1))
        else:
            return ['period parameter error!']

        sql = "SELECT {} as period, parameter2 as device,SUM(parameter1) as amount from k \
                WHERE action = '201' \
                GROUP BY {},parameter2" \
            .format(period,period)
        list = db.session.execute(sql).fetchall()
        print (list)
        i =0
        l = len(list)
        if l == 0:
            return re

        for row in re:
            while row['date'] == list[i][0]:
                row[list[i][1]]=list[i][2]
                if i< (l-1):
                    i +=1
                else:
                    break
        return re

