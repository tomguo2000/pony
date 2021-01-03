from .base_view import BaseView
from application.services.order_service import OrderService
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

            # 增加记录到K线图
            KService_action = '201'
            KService.add_record(action=KService_action,parameter1=data['amount'],parameter2='New',timestamp=int(time.time()))

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
        print (self.parameters)
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
        order_id = self.parameters.get('order_id')
        order = OrderService.get_order(order_id)
        if order.orderStatus == '2':
            if order.thunderserviceStatus != '1':
                if OrderService.make_fulfill(order_id):
                    return{
                             "code":200,
                             "message": "order fulfilled success"
                         },200
                else:
                    return{
                              "code":4011,
                              "message": returncode['4011']
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

class expressorderView(BaseView):
    def process(self):
        orderID = request.args.get('orderID',type=str)

        #按传入的很长的orderID，取出实际的order记录，得到description和amount
        order = OrderService.get_expressorder(orderID)
        productdetail= order.description
        amount=order.amount
        thunderservice_id = order.thunderservice_id

        #根据orderID中记录的thunderservice_id，取到thunderservice信息
        thunderservice = GetThunderservice.get_thunderservice(thunderservice_id)
        subject = thunderservice.membershipEN

        #根据orderID中记录的user_id，取到用户email
        user = UserService.get_user(order.user_id)
        if user:
            useremail= user.email
        else:
            useremail = 'ERROR'

        resp = make_response(render_template('expressorder.html',
                                             productdetail=productdetail,
                                             amount=amount,
                                             subject = subject,
                                             orderid=orderID,
                                             productID = thunderservice_id,
                                             useremail=useremail,
                                             OrderTime = int(time.time())), 200)
        return resp

class addExpressorder(BaseView):
    def process(self):
        from application.services.user_service import UserService
        data = self.parameters.get('body')
        print("addExpressorder:")
        print(data)
        user_info = UserService.get_user(data.get('user_id'))
        if user_info:

            thunderserviceFufeiList = GetThunderservice.get_fufei_thunderservice()
            thunderserviceList = []
            if len(thunderserviceFufeiList):
                for item in thunderserviceFufeiList:
                    temp = {
                        "thunderserviceID":item.id,
                        "price":item.price,
                        "currency":"USD",
                        "duration":item.duration
                    }
                    thunderserviceList.append(temp)

            #生成order_id
            thunderServiceID = data.get('thunderserviceID') if data.get('thunderserviceID') else '3'
            if str(thunderServiceID) not in thunder_service_for_expressorderID['FUFEI']:
                return {
                           "code": 5005,
                           "message": returncode['5005']
                       },401

            order_id = 'EX'+time.strftime("%Y%m%d%H%M%S",time.localtime())+'U'+user_info.email[:1]+'P'+str(thunderServiceID)

            #取出定价，根据coupon，调整amount
            thunderservice_selected = GetThunderservice.get_thunderservice(thunderServiceID)
            amount = thunderservice_selected.price if thunderservice_selected else 0
            coupon = data.get('coupon')
            amount = amount

            #expressorder不需要发送订单邮件
            emailNotification = False

            #取到thunderservice中对应的desc
            description = thunderservice_selected.description if thunderservice_selected else None

            #添加订单记录
            OrderService.add_order(order_id,data['user_id'], thunderServiceID, \
                                   time.time()*1000,coupon,amount,emailNotification,description)
            db.session.commit()

            # 增加记录到K线图
            KService_action = '201'
            KService.add_record(action=KService_action,parameter1=amount,parameter2='New',timestamp=int(time.time()))

            resp = {
                "thunderserviceList":thunderserviceList,
                "selectedThunderServiceID":thunderServiceID,
                "orderID":order_id,
                "qrsource":"/app/expressorder_view?orderID="+order_id
            }
            return resp,200
        else:
            return {
                       "code": 4011,
                       "message": returncode['4011']
                   },401

class appCheckExpressOrderResult(BaseView):
    def process(self):
        data = self.parameters.get('body')
        order_id = data.get('order_id')
        order = OrderService.get_expressorder(order_id)
        if order:
            if order.orderStatus == '2':
                if order.thunderserviceStatus == '1':
                    return{
                              "code":200,
                              "message": "Order paid and thunderservice opened,please refresh your user info"
                          },200
                else:
                    return{
                              "code":201,
                              "message": "Order paid and thunderservice is opening, please wait a second"
                          },200
            else:
                return{
                          "code":202,
                          "message": "Order is waiting for pay"
                      },200
        else:
            return{
                      "code":4013,
                      "message":  returncode['4013']
                  },401
