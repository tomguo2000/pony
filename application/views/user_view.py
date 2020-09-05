from .base_view import BaseView
from application.services.user_service import UserService
from application.services.route_service import RouteService
from application.services.usergroup_service import UserGroupService
from application.services.tracking_service import TrackingService
from application.services.k_service import KService
from application.common.foundation import db
from application.app import flask_app
from flask import request
from application.common.returncode import returncode
import logging
import jwt
import config.settings
import datetime, time
from application.common.dict import thunder_service_name,thunder_service_ID
from application.common.sendmail_sendcloud import send_simple_message


"""
each class is for one API
"""


class GetUserView(BaseView):
    def process(self):
        logging.info("GetUserView. {}".format(self.parameters))
        self.other_function()
        user_id = self.parameters.get('user_id')
        user_info = UserService.get_user(user_id)
        if (user_info):
            user_info1 = {
                'user_id': user_info.id,
                'email': user_info.email,
                'email_verified': user_info.email_verified,
                'account_status': user_info.account_status,
                'register_source': user_info.register_source,
                'register_datetime': user_info.register_datetime,
                'last_login_datetime': user_info.last_login_datetime,
                'last_login_ipaddress': user_info.last_login_ipaddress,
                'affiliate': user_info.affiliate,
                'affiliate_url': "TBD",
                'individual_coupon': user_info.individual_coupon,
                'mentor': user_info.mentor
            }

            user_aff_list = []
            if user_info.affiliate:
                user_aff_users = UserService.get_user_afflist(user_id)
                logging.info("UserSerice.get_user_afflist: {}".format(user_aff_users))
                if user_aff_users:
                    for user in user_aff_users:
                        temp = {
                            "user_id": user.id,
                            "email": user.email,
                            "register_datetime": user.register_datetime,
                            "thunderservice_id": user.thunderservice_id,
                            "thunderservice_endtime": user.thunderservice_endtime
                        }
                        user_aff_list.append(temp)

            return {
                "code": 200,
                "message": "get user info success",
                "userInfo": user_info1,
                "userAff": user_aff_list
            }
        return {
                   "code": 4011,
                   "message": returncode['4011']
               }, 400

    def other_function(self):
        pass


class GetUserServiceView(BaseView):

    def process(self):
        self.other_function()
        user_id = self.parameters.get('user_id')
        user_info = UserService.get_user(user_id)
        thunderservice_password = UserService.get_user_service_password(user_id)
        route_info = RouteService.get_routes_by_group_ID(user_info.usergroup_id)
        logging.info("route_info:{}".format(route_info))
        if (user_info):

            routes = list()
            for route in route_info:
                routes.append({
                    "id": route.id,
                    "usergroup_id": route.usergroup_id,
                    "sequence": route.sequence,
                    "online": route.online,
                    "domain": route.domain,
                    "port": route.port,
                    "servernameEN": route.servernameEN,
                    "servernameCN": route.servernameCN,
                    "password": thunderservice_password.oripassword
                })

            user_service_info = {
                'user_id': user_info.id,
                'thunderservice_id': user_info.thunderservice_id,
                'thunderservice_name': thunder_service_name[str(user_info.thunderservice_id)],
                'thunderservice_starttime': user_info.thunderservice_starttime,
                'thunderservice_endtime': user_info.thunderservice_endtime,
                'usergroup_id': user_info.usergroup_id,
                'thunderservice_oripassword': thunderservice_password.oripassword,
                'thunderservice_client_amount': user_info.thunderservice_client_amount,
                'thunderservice_traffic_amount': user_info.thunderservice_traffic_amount,
                'thunderservice_up_traffic_used': user_info.thunderservice_up_traffic_used,
                'thunderservice_down_traffic_used': user_info.thunderservice_down_traffic_used,
                "routes": routes
            }

            return {
                "code": 200,
                "message": "get user service success",
                "userServiceInfo": user_service_info
            }
        return 'None', 400

    def other_function(self):
        pass

class GetUserOrderView(BaseView):

    def process(self):
        self.other_function()
        user_id = self.parameters.get('user_id')
        user_orders = UserService.get_user_order(user_id)
        # logging.info("route_info:{}".format(route_info))
        if (user_orders):

            orders = list()
            for order in user_orders:
                orders.append({
                    "id": order.id,
                    "placeOrderTime": order.placeOrderTime,
                    "paymentMethod": order.paymentMethod,
                    "paymentTime": order.paymentTime,
                    "paymentSN": order.paymentSN,
                    "amount": order.amount,
                    "orderStatus": order.orderStatus,
                })

            return {
                "code": 200,
                "message": "get user orders success",
                "userOrdersInfo": orders
            }
        return 'None', 400

    def other_function(self):
        pass

class ActiveUserServiceView(BaseView):

    def process(self):
        user_body = self.parameters.get('body')
        user_id = user_body.get('user_id')
        thunderservice_id = user_body.get('thunderservice_id')
        service_start_date = user_body.get('service_start_date')
        service_end_date = user_body.get('service_end_date')
        update_data = {
            "membership": thunderservice_id,
            "membership_starttime": service_start_date,
            "membership_endtime": service_end_date
        }
        user_data = UserService.get_user(user_id)

        # same membership level, update period only
        if user_data.get('membership') == thunderservice_id:
            UserService.modify_user_by_id(user_id, update_data)
            db.session.commit()
            return {
                'result': "User already have same service, modify date only. success"
            }

        # change membership level, delete old pwd and assign a new one
        new_usergroup_id = self.choose_best_usergroup(thunderservice_id)
        print("new_usergroup_id:", new_usergroup_id)

        UserService.delete_assigned_pwd(user_id)
        UserGroupService.decrease(user_data.get('usergroup'))
        update_data = {
            "usergroup": new_usergroup_id,
            "membership": thunderservice_id,
            "membership_starttime": service_start_date,
            "membership_endtime": service_end_date
        }
        UserService.modify_user_by_id(user_id, update_data)

        UserService.assign_new_pwd(user_id, new_usergroup_id)
        UserGroupService.increase(new_usergroup_id)

        db.session.commit()
        return {
            'result': "Active thunderservice success"
        }

    def choose_best_usergroup(self, thunderservice_id):
        data = UserGroupService.get_allusergroup()
        group_list = []
        for row in data:
            if thunderservice_id in row.get('which_service'):
                temp = row.get('current_capacity') / row.get('maxcapacity'), row.get('id')
                group_list.append(temp)
                print(row)

        group_list.sort(reverse=True)
        if group_list:
            return group_list.pop()[1]
        else:
            return None


class GetUsersView(BaseView):
    def process(self):
        pageNum = request.args.get('pageNum', 1, type=int)
        pageSize = request.args.get('pageSize', 10, type=int)
        logging.info("GetUsersView. pageNum:{},pageSize:{}".format(pageNum, pageSize))

        totals = UserService.get_user_amount() - 1
        totalPages = (totals + pageSize - 1) // pageSize
        users = UserService.get_users(pageNum, pageSize)
        usersview = list()
        for user in users:
            # print (user)  #(<UserModel 1>, <ThunderserviceModel 1>)
            usersview.append({
                'user_id': user.UserModel.id,
                'user_register_source': user.UserModel.register_source,
                'user_email': user.UserModel.email,
                'user_email_verified': user.UserModel.email_verified,
                'user_register_datetime': user.UserModel.register_datetime,
                'user_thunderservice': user.UserModel.thunderservice_id,
                'user_usergroup': user.UserModel.usergroup_id,
                'user_account_status': user.UserModel.account_status,
                'user_service_endtime': user.UserModel.thunderservice_endtime,
                'user_thunderservice_name': user.ThunderserviceModel.membershipCN
            })
        return {
            "code": 200,
            "message": "get users success",
            "results": {
                "totals": totals,
                "totalPages": totalPages,
                "list": usersview
            }
        }


class DeleteUserView(BaseView):

    def process(self):
        return "success"


class ModifyUserViewByID(BaseView):
    def process(self):
        user_body = self.parameters.get('body')
        user_id = self.parameters.get('user_id')
        current_userdata = UserService.get_user(user_id)
        if current_userdata:
            if user_body.get('id'):
                return {
                           "code": 4012,
                           "message": returncode['4012']
                       }, 400
            logging.info("ModifyUserViewByID. UserService.modify_user_by_id:{}{}".format(user_id, user_body))
            if user_body.get('usergroup_id'):
                if current_userdata.usergroup_id != user_body.get('usergroup_id'):
                    old_usergroup_id = current_userdata.usergroup_id
                    new_usergroup_id = user_body.get('usergroup_id')
                    logging.info("UserID:{},need change usergroup_id from {} to {}".format(user_id, old_usergroup_id,
                                                                                           new_usergroup_id))
                    UserService.delete_assigned_pwd(user_id)
                    UserGroupService.decrease(old_usergroup_id)
                    UserService.assign_new_pwd(user_id, new_usergroup_id)
                    UserGroupService.increase(new_usergroup_id)

            UserService.modify_user_by_id(user_id, user_body)
            db.session.commit()
            return {
                "code": 200,
                "message": "modify user success"
            }

        else:
            return {
                       "code": 4011,
                       "message": returncode['4011']
                   }, 400


# class ModifyUserView(BaseView):
#
#     def process(self):
#         user_body = self.parameters.get('body')
#         if UserService.get_user_by_email(user_body.get('email')):
#             #body里传入email和任意字段，怎么写任意字段的修改
#             UserService.modify_user(user_body.get('name'),user_body.get('email'))
#             db.session.commit()
#             return "modify user success"
#         else:
#             return "user not exist",400

class AddUserView(BaseView):

    def process(self):
        user_body = self.parameters.get('body')

        if self.check_registed_user_by_email(user_body.get('email')):
            return {
                       "code": 4010,
                       "message": returncode['4010'],
                   }, 400
        logging.info("AddUserView. {}".format(user_body))
        UserService.add_user(user_body.get('name'), user_body.get('email'), user_body.get('password'),
                             user_body.get('source'), user_body.get('email_verified'), time.time() * 1000)
        db.session.commit()
        if not user_body['email_verified']:
            logging.error("email_verified false, So we need send an verify email to {}".format(user_body['email']))

        # get user service info again, active it.
        user = UserService.get_user_by_email(user_body.get('email'))
        UserService.active_thunderservice(user.id, user.thunderservice_id, user.thunderservice_starttime,
                                          user.thunderservice_endtime)
        db.session.commit()

        source = user_body.get('source') if user_body.get('source') else 'Unknown'
        KService_action = '101'
        KService.add_record(action=KService_action,parameter1=user.id,parameter2=source,timestamp=int(time.time()))

        return {
            "code": 200,
            "message": "add user success",
        }

    def check_registed_user_by_email(self, user_email):
        if UserService.get_user_by_email(user_email):
            return True


class UserLoginView(BaseView):
    def process(self):
        trackinginput = self.parameters.get('body')
        user_body = self.parameters.get('body')
        user = UserService.get_user_by_email(user_body['email'])

        logging.info("UserLoginView,email:{}".format(user_body['email']))
        if not user:
            return {
                       "code": 4001,
                       "message": returncode['4001'],
                   }, 401

        if (user_body['password'] == user.password):
        # if user.check_password(user_body['password']):
            token = jwt.encode(
                {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1000)},
                flask_app.config['SECRET_KEY'])
            refreshToken = jwt.encode({'user_id': user.id, 'type': 'refresh',
                                       'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=14400)},
                                      flask_app.config['SECRET_KEY'])
            UserService.save_token(user.id, token, refreshToken)
            db.session.commit()

            pwresource = UserService.get_user_service_password(user.id)
            if pwresource:
                thunderservice_password = pwresource.oripassword
            else:
                thunderservice_password = 'glnvod'  # 万一没有，就拿这个顶
                logging.info(
                    "UserLoginView. This user :{} do not have thunderservice password, use reserved insteed".format(
                        user_body['email']))

            routes = RouteService.get_routes_by_group_ID(user.usergroup_id)

            routes_info = list()
            for route in routes:
                routes_info.append({
                    'id': route.id,
                    'usergroup_id': route.usergroup_id,
                    'sequence': route.sequence,
                    'online': route.online,
                    'domain': route.domain,
                    'port': route.port,
                    # 'ipaddress': route.ipaddress,
                    'servernameEN': route.servernameEN,
                    'servernameCN': route.servernameCN,
                    # 'routeStarttime': route.routeStarttime,
                    # 'trafficLimit': route.trafficLimit,
                    # 'trafficUsed': route.trafficUsed,
                    # 'trafficResetDay': route.trafficResetDay,
                    'password': thunderservice_password
                })
            trackingoutput = "成功"
            TrackingService.tracking(trackinginput,trackingoutput, user.id)

            device = user_body.get('device') if user_body.get('device') else 'Unknown'
            thunderservice = user.thunderservice_id
            # if thunderservice in (thunder_service_ID['LOW_SPEED'] or thunder_service_ID['TRIAL']):
            KService_action = '102'
            # thunderservice exits and is a VIP
            if thunderservice and str(thunderservice) in thunder_service_ID['FUFEI']:
                KService_action = '103'
            KService.add_record(action=KService_action,parameter1=user.id,parameter2=device,timestamp=int(time.time()))

            return {
                "code": 200,
                "message": "login success",
                "results": {
                    "user": {
                        "user_id": user.id,
                        "thunderservice_id": user.thunderservice_id,
                        "thunderservice_endtime": user.thunderservice_endtime,
                        "usergroup_id": user.usergroup_id
                    },
                    "routes": routes_info,
                    "credential": {
                        "token": token.decode('UTF-8'),
                        "refreshToken": refreshToken.decode('UTF-8')
                    }
                }
            }

        return {
                   "code": 4002,
                   "message": returncode['4002'],
               }, 401

    def check_registed_user_by_email(self, user_email):
        if UserService.get_user_by_email(user_email):
            return True

class ResetPasswordView(BaseView):

    def process(self):
        email = request.args.get('email')
        user = UserService.get_user_by_email(email)

        if user:
            #TODO Check if user_id is currently logged in
            reset_token = jwt.encode({'user_id': user.id,'action':'resetpassword', 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},
            flask_app.config['SECRET_KEY'])
            reset_token = reset_token.decode("utf-8")
            print(reset_token)
            # send email to customer
            # if (send_simple_message(email,"重置密码",reset_token))==200:
            #     return {"code":200,"message":"Send email success"}
            # else:
            #     return{"code":4025,"message":returncode['4025']},401
        else:
            return {"code": 4001,"message": returncode['4001'],}, 401

class PwdResetTokenView(BaseView):
    def process(self):
        body = self.parameters.get('body')
        print("body:",body)
        reset_token = body['reset_token']
        newpassword = body['newpassword']
        try:
            data = jwt.decode(reset_token, config.settings.SECRET_KEY)
            if data.get('action')!= 'resetpassword':
                return {"code": 4004,"message": returncode['4004'],}, 401
            if UserService.get_user(data['user_id']):
                UserService.user_pwdreset_submit(data['user_id'],newpassword)
                db.session.commit()
            else:
                return {"code": 4004,"message": returncode['4004'],}, 401
        except:
            return {"code": 4004,"message": returncode['4004'],}, 401