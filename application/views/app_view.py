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
from application.common.dict import thunder_service_name,thunder_service_nameEN,thunder_service_ID
from application.common.sendmail_sendcloud import send_simple_message


class AppRegisterUserView(BaseView):

    def process(self):
        user_body = self.parameters.get('body')

        if self.check_registed_user_by_email(user_body.get('email')):
            return {
                       "code": 4010,
                       "message": returncode['4010'],
                   }, 400
        logging.info("AddUserView. {}".format(user_body))
        UserService.add_user(user_body.get('name'), user_body.get('email'), user_body.get('password'),
                             user_body.get('appkey'), user_body.get('email_verified'), int(time.time()))
        db.session.commit()
        if not user_body.get('email_verified'):
            logging.error("email_verified false, So we need send an verify email to {}".format(user_body['email']))

        # get user service info again, active it.
        user = UserService.get_user_by_email(user_body.get('email'))
        UserService.active_thunderservice(user.id, user.thunderservice_id, user.thunderservice_starttime,
                                          user.thunderservice_endtime)
        db.session.commit()

        source = user_body.get('appkey') if user_body.get('appkey') else 'Unknown'
        KService_action = '101'
        KService.add_record(action=KService_action,parameter1=user.id,parameter2=source,timestamp=int(time.time()))

        return {
            "code": 200,
            "message": "add user success",
        }

    def check_registed_user_by_email(self, user_email):
        if UserService.get_user_by_email(user_email):
            return True


class AppUserLoginView(BaseView):
    def process(self):
        trackinginput = self.parameters.get('body')
        user_body = self.parameters.get('body')
        user = UserService.get_user_by_email(user_body['email'])

        logging.info("AppUserLoginView,email:{}".format(user_body['email']))
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
                    "AppUserLoginView. This user :{} do not have thunderservice password, use reserved insteed".format(
                        user_body['email']))

            if str(user.thunderservice_id) not in thunder_service_ID['FUFEI']:
                thunderservice_password = 'glnvod'

            routes = RouteService.get_routes_by_group_ID(user.usergroup_id)

            routes_info = list()
            for route in routes:
                routes_info.append({
                    'id': route.id,
                    'servernameEN': route.servernameEN,
                    'servernameCN': route.servernameCN,
                    'remoteAddr': route.domain,
                    'remotePort': route.port,
                    'password': thunderservice_password,
                    "ipv6":route.ipv6,
                    "statusCN": "正常",
                    "statusEN": "Available"
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

            thunderservice_name = thunder_service_name[str(thunderservice)]

            user_info = {
                "user_id": user.id,
                "name": user.email,
                "period":time.strftime("%Y-%m-%d", time.localtime(user.thunderservice_endtime)),
                "invitationcode":user.individual_coupon,
                "client_group_id": user.thunderservice_id,
                "vip":thunderservice_name,
                "vip_en":thunder_service_nameEN[str(thunderservice)],
                "vip_level":user.usergroup_id,
                "validtime":2
            }

            return {
                "code": 200,
                "message": "login success",
                "results": {
                    "user_info": user_info,
                    "ips": routes_info,
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


class AppGetUserView(BaseView):
    def process(self):
        # user_body = self.parameters.get('body')
        user_id = request.args.get('user_id')
        user = UserService.get_user(user_id)

        logging.info("AppGetUserView,id:{}".format(user_id))
        if not user:
            return {
                       "code": 4001,
                       "message": returncode['4001'],
                   }, 401

        pwresource = UserService.get_user_service_password(user.id)

        if pwresource:
            thunderservice_password = pwresource.oripassword
        else:
            thunderservice_password = 'glnvod'  # 万一没有，就拿这个顶
            logging.info(
                "AppUserLoginView. This user :{} do not have thunderservice password, use reserved insteed".format(
                    user_id))

        if str(user.thunderservice_id) not in thunder_service_ID['FUFEI']:
            thunderservice_password = 'glnvod'

        routes = RouteService.get_routes_by_group_ID(user.usergroup_id)

        routes_info = list()
        for route in routes:
            routes_info.append({
                'id': route.id,
                'servernameEN': route.servernameEN,
                'servernameCN': route.servernameCN,
                'remoteAddr': route.domain,
                'remotePort': route.port,
                'password': thunderservice_password,
                "ipv6":route.ipv6,
                "statusCN": "正常",
                "statusEN": "Available"
            })

        thunderservice_name = thunder_service_name[str(user.thunderservice_id)]
        thunderservice_nameEN = thunder_service_nameEN[str(user.thunderservice_id)]

        user_info = {
            "user_id": user.id,
            "name": user.email,
            "period":time.strftime("%Y-%m-%d", time.localtime(user.thunderservice_endtime)),
            "invitationcode":user.individual_coupon,
            "client_group_id": user.thunderservice_id,
            "vip":thunderservice_name,
            "vip_en":thunderservice_nameEN,
            "vip_level":user.usergroup_id,
            "validtime":2
        }

        return {
            "code": 200,
            "message": "get user info success",
            "results": {
                "user_info": user_info,
                "ips": routes_info
            }
        }

class AppRefreshTokenView(BaseView):
    def process(self):
        trackinginput = self.parameters.get('body')
        user_body = self.parameters.get('body')
        print (user_body)
        try:
            user_id = user_body.get('user_id')
            refreshToken = user_body.get('refreshToken')
        except:
            return {
                       "code": 5004,
                       "message": returncode['5004'],
                   }, 401

        user = UserService.get_user(user_id)

        if not user:
            return {
                       "code": 4011,
                       "message": returncode['4011'],
                   }, 401

        print (refreshToken)
        print (user.refreshToken)
        if (refreshToken == user.refreshToken):
            token = jwt.encode(
                {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
                flask_app.config['SECRET_KEY'])
            refreshToken = jwt.encode({'user_id': user.id, 'type': 'refresh',
                                       'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=14400)},
                                      flask_app.config['SECRET_KEY'])
            UserService.save_token(user.id, token, refreshToken)
            db.session.commit()

            trackingoutput = "刷新token成功"
            TrackingService.tracking(trackinginput,trackingoutput, user.id)

            thunderservice_name = thunder_service_name[str(user.thunderservice_id)]
            thunderservice_nameEN = thunder_service_nameEN[str(user.thunderservice_id)]

            user_info = {
                "user_id": user.id,
                "name": user.email,
                "period":time.strftime("%Y-%m-%d", time.localtime(user.thunderservice_endtime)),
                "invitationcode":user.individual_coupon,
                "client_group_id": user.thunderservice_id,
                "vip":thunderservice_name,
                "vip_en":thunderservice_nameEN,
                "vip_level":user.usergroup_id,
                "validtime":2
            }

            return {
                "code": 200,
                "message": "refresh token success",
                "results": {
                    "user_info": user_info,
                    "credential": {
                        "token": token.decode('UTF-8'),
                        "refreshToken": refreshToken.decode('UTF-8')
                    }
                }
            }

        return {
                   "code": 4005,
                   "message": returncode['4005'],
               }, 401

    def check_registed_user_by_email(self, user_email):
        if UserService.get_user_by_email(user_email):
            return True



class AppGetAnnouncementView(BaseView):
    def process(self):
        user_id = request.args.get('user_id')
        user = UserService.get_user(user_id)

        logging.info("AppGetAnnouncementView,id:{}".format(user_id))
        if not user:
            return {
                       "code": 4001,
                       "message": returncode['4001'],
                   }, 401

        return {
            "code": 200,
            "message": "get Announcement success",
            "results": dict(announcement="胡子长了吗？后面是一个回车换行。\n"
                                         "这里是第二行，显示的咋样？")
        }

class AppFeedbackView(BaseView):
    def process(self):
        trackinginput = self.parameters.get('body')
        user_body = self.parameters.get('body')
        print (user_body)
        try:
            user_id = user_body.get('user_id')
            diagnoses = user_body.get('diagnoses')
            feedback = user_body.get('feedback')
        except:
            return {
                       "code": 5004,
                       "message": returncode['5004'],
                   }, 401

        trackingoutput = "接收feedback成功"
        TrackingService.tracking(trackinginput,trackingoutput, user_id)

        return {
            "code": 200,
            "message": "post feedback success",
            "results": {
            }
        }
