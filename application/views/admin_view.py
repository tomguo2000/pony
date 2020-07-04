from .base_view import BaseView
from application.services.user_service import UserService
from application.services.route_service import RouteService
from application.services.usergroup_service import UserGroupService
from application.services.tracking_service import TrackingService
from application.common.foundation import db
from application.app import flask_app
from flask import request
from application.common.returncode import returncode
import logging
import datetime, time
from application.common.dict import thunder_service_name

"""
each class is for one API
"""


class searchTrackingView(BaseView):
    def process(self):
        data = request.get_json()
        if not data.get('pager'):
            pageNum = 1
            pageSize =10
        else:
            if data['pager'].get('pageNum'):
                pageNum = data['pager']['pageNum']
            else:
                pageNum = 1

            if data['pager'].get('pageSize'):
                pageSize = data['pager']['pageSize']
            else:
                pageSize = 10

        if data.get('searchData'):
            userID = data['searchData'].get('userID')
            content = data['searchData'].get('content')
            result = data['searchData'].get('result')
        else:
            userID = None
            content = None
            result = None

        list= TrackingService.search(pageNum,pageSize,userID,content,result)

        return (list)





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
        print("1", time.time() * 1000)
        user_body = self.parameters.get('body')
        user = UserService.get_user_by_email(user_body['email'])

        print("2", time.time() * 1000)

        logging.info("UserLoginView,email:{}".format(user_body['email']))
        if not user:
            return {
                       "code": 4001,
                       "message": returncode['4001'],
                   }, 401

        if (user_body['password'] == user.password):
            # if user.check_password(user_body['password']):
            print("3", time.time() * 1000)
            token = jwt.encode(
                {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1000)},
                flask_app.config['SECRET_KEY'])
            refreshToken = jwt.encode({'user_id': user.id, 'type': 'refresh',
                                       'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=14400)},
                                      flask_app.config['SECRET_KEY'])
            UserService.save_token(user.id, token, refreshToken)
            db.session.commit()
            print("4", time.time() * 1000)

            pwresource = UserService.get_user_service_password(user.id)
            if pwresource:
                thunderservice_password = pwresource.oripassword
            else:
                thunderservice_password = 'glnvod'  # 万一没有，就拿这个顶
                logging.info(
                    "UserLoginView. This user :{} do not have thunderservice password, use reserved insteed".format(
                        user_body['email']))

            print("5", time.time() * 1000)

            routes = RouteService.get_routes_by_group_ID(user.usergroup_id)

            print("6", time.time() * 1000)

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
            print("7", time.time() * 1000)
            trackingoutput = "成功"
            TrackingService.tracking(trackinginput,trackingoutput, user.id)
            print("8", time.time() * 1000)
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
