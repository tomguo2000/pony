from .base_view import BaseView
from application.services.order_service import OrderService
from application.common.foundation import db
import time
from application.common.returncode import returncode
from flask import request
import logging



"""
each class is for one API
"""
class GetOrderView(BaseView):
    def process(self):
        order_id = self.parameters.get('order_id')
        logging.info("GetOrderView. order_id:{}".format(order_id))
        order = OrderService.get_order(order_id)
        if (order):
            order_info = {
                'order_id': order.id,
                "user_id": order.user_id,
                "thunderservice_id" : order.thunderservice_id,
                "placeOrderTime" : order.placeOrderTime,
                "coupon": order.coupon,
                "paymentMethod": order.paymentMethod,
                "paymentTime": order.paymentTime,
                "paymentSN": order.paymentSN,
                "emailNotification": order.emailNotification,
                "amount":order.amount,
                "orderStatus":order.orderStatus,
                "thunderserviceStatus":order.thunderserviceStatus
            }

            return {
                "code": 200,
                "message": "get order success",
                "results": order_info
            }
        return {
            "code": 4013,
            "message": returncode['4013']
        },400

class GetOrdersView(BaseView):
    def process(self):
        pageNum = request.args.get('pageNum', 1, type=int)
        pageSize = request.args.get('pageSize', 10, type=int)
        logging.info("GetOrdersView. pageNum:{},pageSize:{}".format(pageNum, pageSize))

        totals = OrderService.get_order_amount()
        totalPages = (totals + pageSize - 1) // pageSize
        orders = OrderService.get_orders(pageNum, pageSize)
        ordersview = list()
        for order in orders:
            ordersview.append({
                'order_id': order.id,
                "user_id": order.user_id,
                "thunderservice_id" : order.thunderservice_id,
                "placeOrderTime" : order.placeOrderTime,
                "coupon": order.coupon,
                "paymentMethod": order.paymentMethod,
                "paymentTime": order.paymentTime,
                "paymentSN": order.paymentSN,
                "emailNotification": order.emailNotification,
                "amount":order.amount,
                "orderStatus":order.orderStatus,
                "thunderserviceStatus":order.thunderserviceStatus
            })
        return {
            "code": 200,
            "message": "get orders success",
            "results": {
                "totals": totals,
                "totalPages": totalPages,
                "list": ordersview
            }
        }

class AddOrderView(BaseView):
    def process(self):
        from application.services.user_service import UserService
        data = self.parameters.get('body')
        print("AddOrderView:")
        print(data)
        user_info = UserService.get_user(data['user_id'])
        if user_info:
            OrderService.add_order(data['user_id'], data['thunderservice_id'],\
                                   time.time()*1000,data['coupon'],data['amount'],data['emailNotification'])
            db.session.commit()
            return {
                "code":200,
                "message":"Add order success"
            }
        else:
            return {
                "code": 4011,
                "message": returncode['4011']
            },401

class DeleteOrderView(BaseView):
    def process(self):
        order_id = self.parameters.get('order_id')
        order_data = OrderService.get_order(order_id)
        if order_data:
            OrderService.delete_order(order_id)
            db.session.commit()
            return{
                "code":200,
                "message":"delete success"
            }
        else:
            return{
                "code":4013,
                "message": returncode['4013']
            } ,401


class CancelOrderView(BaseView):
    def process(self):
        order_id = self.parameters.get('order_id')
        order_data = OrderService.get_order(order_id)
        if order_data:
            if order_data.thunderserviceStatus == "1":
                return{
                          "code":4015,
                          "message": returncode['4015']
                      } ,400
            else:
                OrderService.cancel_order(order_id)
                return{
                    "code":200,
                    "message":"Cancel this order success"
            }
        else:
            return{
                "code":4013,
                "message": returncode['4013']
            } ,400


class MarkOrderPaidView(BaseView):
    def process(self):
        order_id = self.parameters.get('order_id')
        order_data = OrderService.get_order(order_id)
        if order_data:
            OrderService.mark_paid_order(order_id)
            db.session.commit()
            return{
                "code":200,
                "message":"Mark this order as paid success"
            },200
        else:
            return{
                "code":4013,
                "message": returncode['4013']
            },401


class FulfillOrderView(BaseView):
    def process(self):
        from application.services.user_service import UserService
        order_id = self.parameters.get('order_id')
        order = OrderService.get_order(order_id)
        if order.orderStatus == '2':
            if order.thunderserviceStatus != '1':
                user = UserService.get_user(order.user_id)
                if user:
                    from application.models.thunderservice_model import ThunderserviceModel
                    if user.thunderservice_id == order.thunderservice_id:

                        # 相同的thunderservice，只修改到期时间
                        thunderservice = ThunderserviceModel.query.filter(ThunderserviceModel.id == order.thunderservice_id).first()
                        duration = thunderservice.duration*86400*1000
                        user.thunderservice_endtime =  user.thunderservice_endtime+duration

                        # 标记本order已经完成了
                        OrderService.mark_fulfilled(order_id)
                        db.session.commit()

                        return{
                                  "code":200,
                                  "message":"Fulfill this order success"
                              },200
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

                        OrderService.mark_fulfilled(order_id)
                        db.session.commit()
                        return{
                                  "code":200,
                                  "message":"Fulfill this order success"
                        },200
                else:
                    return {
                        "code":4011,
                        "message": returncode['4011']
                    },400
            else:
                return {
                    "code": 4014,
                    "message": returncode['4014']
                },400
        elif order:
            return{
                      "code":4016,
                      "message": returncode['4016']
                  },400
        else:
            return{
                "code":4013,
                "message": returncode['4013']
            },400