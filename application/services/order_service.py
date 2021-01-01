from .base_service import BaseService
from application.models.order_model import OrderModel
from application.services.k_service import KService
from application.common.foundation import db
from sqlalchemy import between,func
import time


class OrderService(BaseService):
    @staticmethod
    def add_order(order_id,user_id,thunderservice_id,placeOrderTime,coupon,amount,emailNotification,description):
        print (user_id,thunderservice_id,placeOrderTime,coupon,amount,emailNotification,description)
        order = OrderModel(
            order_id = order_id,
            user_id = user_id,
            thunderservice_id = thunderservice_id,
            placeOrderTime = placeOrderTime,
            coupon = coupon,
            amount = amount,
            emailNotification = emailNotification,
            description = description,
            orderStatus = '1'
        )
        db.session.add(order)


    @staticmethod
    def delete_order(order_id):
        OrderModel.query.filter(OrderModel.id == order_id).delete()


    @staticmethod
    def cancel_order(order_id):
        order = OrderModel.query.filter(OrderModel.id == order_id).first()
        if order.orderStatus == None or order.orderStatus == '1' :
            order.orderStatus = '3'
            db.session.commit()
            return True
        else:
            return False

    @staticmethod
    def mark_paid_order(order_id):
        order = OrderModel.query.filter(OrderModel.id == order_id).first()
        # mark order as paid
        order.orderStatus = '2'

    @staticmethod
    def make_fulfill(order_id):
        from application.services.user_service import UserService
        order = OrderModel.query.filter(OrderModel.id == order_id).first()
        user = UserService.get_user(order.user_id)
        if user:
            from application.models.thunderservice_model import ThunderserviceModel
            if user.thunderservice_id == order.thunderservice_id:

                # 相同的thunderservice，只修改到期时间
                thunderservice = ThunderserviceModel.query.filter(ThunderserviceModel.id == order.thunderservice_id).first()
                duration = thunderservice.duration*86400*1000
                user.thunderservice_endtime =  user.thunderservice_endtime+duration

                # 标记本order已经完成了
                order.thunderserviceStatus = '1'
                db.session.commit()

                # 增加记录到K线图
                KService_action = '201'
                KService.add_record(action=KService_action,parameter1=order.amount,parameter2='Paid',timestamp=int(time.time()))

                return True
            else:
                thunderservice = ThunderserviceModel.query.filter(ThunderserviceModel.id == order.thunderservice_id).first()
                user_updatedata={
                    "thunderservice_id":order.thunderservice_id,
                    "thunderservice_client_amount":thunderservice.defaultClientAmount,
                    "thunderservice_traffic_amount":thunderservice.defaultTrafficAmount,
                }
                thunderservice_starttime = time.time()*1000
                thunderservice_endtime   = time.time()*1000
                if thunderservice.id != 1:
                    thunderservice_endtime = thunderservice_endtime + thunderservice.duration*86400*1000

                UserService.modify_user_by_id(order.user_id,update_data=user_updatedata)
                UserService.active_thunderservice(order.user_id,order.thunderservice_id,thunderservice_starttime,thunderservice_endtime)
                db.session.commit()

                order.thunderserviceStatus = '1'
                db.session.commit()

                # 增加记录到K线图
                KService_action = '201'
                KService.add_record(action=KService_action,parameter1=order.amount,parameter2='Paid',timestamp=int(time.time()))
                return True
        else:
            return False


    @staticmethod
    def get_order_amount():
        orderAmount = OrderModel.query.filter().count()
        return orderAmount if orderAmount else 0

    @staticmethod
    def get_orders(pageNum,pageSize):
        orders = OrderModel.query.filter().limit(pageSize).offset((pageNum-1)*pageSize)
        return orders

    @staticmethod
    def get_order(order_id):
        order = OrderModel.query.filter(OrderModel.id == order_id).first()
        return order if order else None

    @staticmethod
    def get_expressorder(expressorder_id):
        order = OrderModel.query.filter(OrderModel.order_id == expressorder_id).first()
        return order if order else None

    @staticmethod
    def modify_order_by_id(order_id,update_data):
        update = OrderModel.query.filter(OrderModel.id == order_id).first()
        for key in update_data:
            setattr(update,key,update_data[key])

    @staticmethod
    def get_order_sum(start,end):
        orderSum = OrderModel.query(func.sum(OrderModel.amount)).filter(between(OrderModel.placeOrderTime,start*1000,end*1000)).all()
        return orderSum if orderSum else 0

    @staticmethod
    def get_paidOrder_sum(start,end):
        # paidOrderSum = OrderModel.query(func.sum(OrderModel.amount)).filter(between(OrderModel.placeOrderTime,start*1000,end*1000)).scalar()

        sql = "SELECT SUM(amount) as amount from orders \
                WHERE orderStatus = '2' AND  \
                placeOrderTime between {} and {}" \
            .format(start*1000,end*1000)
        list = db.session.execute(sql).fetchall()
        paidOrderSum =float('%.2f' % list[0][0])
        return paidOrderSum if paidOrderSum else 0