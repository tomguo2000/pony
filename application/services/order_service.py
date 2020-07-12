from .base_service import BaseService
from application.models.user_model import UserModel
from application.models.thunderservice_model import ThunderserviceModel
from application.models.order_model import OrderModel
from application.models.tracking_model import TrackingModel
from application.common.foundation import db
import logging


class OrderService(BaseService):
    @staticmethod
    def add_order(user_id,thunderservice_id,placeOrderTime,coupon,amount,emailNotification):
        print (user_id,thunderservice_id,placeOrderTime,coupon,amount,emailNotification)
        order = OrderModel(
            user_id = user_id,
            thunderservice_id = thunderservice_id,
            placeOrderTime = placeOrderTime,
            coupon = coupon,
            amount = amount,
            emailNotification = emailNotification,
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
        from application.services.user_service import UserService
        order = OrderModel.query.filter(OrderModel.id == order_id).first()
        # mark order as paid
        order.orderStatus = '2'

    @staticmethod
    def mark_fulfilled(order_id):
        from application.services.user_service import UserService
        order = OrderModel.query.filter(OrderModel.id == order_id).first()
        # mark order as fulfilled
        order.thunderserviceStatus = '1'

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
    def modify_order_by_id(order_id,update_data):
        update = OrderModel.query.filter(OrderModel.id == order_id).first()
        for key in update_data:
            setattr(update,key,update_data[key])

