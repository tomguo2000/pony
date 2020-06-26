from .base_view import BaseView
from application.services.user_service import UserService
from application.services.route_service import RouteService
from application.services.usergroup_service import UserGroupService
from application.common.foundation import db
from application.app import flask_app
from flask import request
from application.common.returncode import returncode
import logging
import jwt
import datetime,time

"""
each class is for one API
"""


class GetUserView(BaseView):

    def process(self):
        self.other_function()
        user_id = self.parameters.get('user_id')
        user_info = UserService.get_user(user_id)
        if (user_info):
            return {
                'id': user_info.get('id'),
                'name': user_info.get('name'),
                'account_status': user_info.get('account_status'),
                'register_source': user_info.get('register_source'),
                'email': user_info.get('email'),
                'email_verified': user_info.get('email_verified'),
                'usergroup_id': user_info.get('usergroup_id'),
                'thunderservice_id':user_info.get('thunderservice_id'),
                'service_starttime': user_info.get('service_starttime'),
                'service_endtime': user_info.get('service_endtime')
            }
        return 'None',400

    def other_function(self):
        pass


class GetUserServiceView(BaseView):

    def process(self):
        self.other_function()
        user_id = self.parameters.get('user_id')
        user_info = UserService.get_user(user_id)
        user_service_password = UserService.get_user_service_password(user_id)
        route_info = RouteService.get_routes_by_group_ID(user_info.get('usergroup'))
        if (user_info):
            return {
                'user_id': user_info.get('id'),
                'user_name': user_info.get('name'),
                'user_email': user_info.get('email'),
                'user_password': user_info.get('password11'),
                'user_usergroup': user_info.get('usergroup'),
                'user_membership': user_info.get('membership'),
                'user_membership_starttime': user_info.get('membership_starttime'),
                'user_membership_endtime': user_info.get('membership_endtime'),
                'user_service_oripassword': user_service_password.get('oripassword'),
                'user_service_hashedpassword': user_service_password.get('hashedpassword'),
                'route_info':route_info
            }
        return 'None',400

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
            "membership":thunderservice_id,
            "membership_starttime":service_start_date,
            "membership_endtime":service_end_date
        }
        user_data = UserService.get_user(user_id)

        #same membership level, update period only
        if user_data.get('membership')==thunderservice_id:
            UserService.modify_user_by_id(user_id,update_data)
            db.session.commit()
            return {
                'result':"User already have same service, modify date only. success"
            }

        #change membership level, delete old pwd and assign a new one
        new_usergroup_id = self.choose_best_usergroup(thunderservice_id)
        print ("new_usergroup_id:",new_usergroup_id)

        UserService.delete_assigned_pwd(user_id)
        UserGroupService.decrease(user_data.get('usergroup'))
        update_data = {
            "usergroup":new_usergroup_id,
            "membership":thunderservice_id,
            "membership_starttime":service_start_date,
            "membership_endtime":service_end_date
        }
        UserService.modify_user_by_id(user_id,update_data)



        UserService.assign_new_pwd(user_id,new_usergroup_id)
        UserGroupService.increase(new_usergroup_id)

        db.session.commit()
        return {
            'result':"Active thunderservice success"
        }
    def choose_best_usergroup(self,thunderservice_id):
        data = UserGroupService.get_allusergroup()
        group_list=[]
        for row in data:
            if thunderservice_id in row.get('which_service'):
                temp = row.get('current_capacity')/row.get('maxcapacity'),row.get('id')
                group_list.append(temp)
                print (row)

        group_list.sort(reverse = True)
        if group_list:
            return group_list.pop()[1]
        else:
            return None



class GetUsersView(BaseView):
    def process(self):
        pageNum = request.args.get('pageNum', 1, type=int)
        pageSize = request.args.get('pageSize', 10, type=int)
        logging.info("GetUsersView. pageNum:{},pageSize:{}".format(pageNum,pageSize))

        totals = UserService.get_user_amount()
        totalPages = (totals + pageSize -1 ) // pageSize
        users = UserService.get_users(pageNum,pageSize)
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
            "code":200,
            "message":"get users success",
            "results":{
                "totals": totals,
                "totalPages":totalPages,
                "list":usersview
            }
        }

class DeleteUserView(BaseView):

    def process(self):
        return "success"

class ModifyUserViewByID(BaseView):

    def process(self):
        user_body = self.parameters.get('body')
        user_id = self.parameters.get('user_id')
        user_current_data = UserService.get_user(user_id)
        if user_current_data:
            if user_body.get('id'):
                return "Id can not be modify",400
            UserService.modify_user_by_id(user_id,user_body)
            db.session.commit()
            return "modify user success"
        else:
            return "user not exist",400

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
                "code":4010,
                "message": returncode['4010'],
            } ,400

        UserService.add_user(user_body.get('name'),user_body.get('email'),user_body.get('password'),user_body.get('source'),time.time()*1000)
        db.session.commit()

        #get user service info again, active it.
        user = UserService.get_user_by_email(user_body.get('email'))
        UserService.active_thunderservice(user.id,user.thunderservice_id,user.thunderservice_starttime,user.thunderservice_endtime)
        db.session.commit()

        return {
            "code":200,
            "message":"add user success",
        }

    def check_registed_user_by_email(self,user_email):
        if UserService.get_user_by_email(user_email):
            return True


class UserLoginView(BaseView):
    def process(self):
        user_body = self.parameters.get('body')
        user = UserService.get_user_by_email(user_body['email'])

        logging.info ("UserLoginView,email:{}".format(user_body['email']))
        if not user:
            return {
                "code":4001,
                "message": returncode['4001'],
            },401

        # if (user_body['password'] == user['password']):
        if user.check_password(user_body['password']):
            token = jwt.encode({'user_id':user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1000) },flask_app.config['SECRET_KEY'])
            refreshToken = jwt.encode({'user_id':user.id, 'type':'refresh','exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=14400) },flask_app.config['SECRET_KEY'])
            UserService.save_token(user.id,token,refreshToken)
            db.session.commit()

            pwresource = UserService.get_user_service_password(user.id)
            if pwresource:
                thunderservice_password = pwresource.oripassword
            else:
                thunderservice_password = 'glnvod'     #万一没有，就拿这个顶
                logging.info("UserLoginView. This user :{} do not have thunderservice password, use reserved insteed".format(user_body['email']))

            routes = RouteService.get_routes_by_group_ID(user.usergroup_id)
            routes_info = list()
            for route in routes:
                routes_info.append({
                    'id': route.id,
                    'usergroup_id': route.usergroup_id,
                    'sequence': route.sequence,
                    'online': route.online,
                    'domain': route.domain,
                    'ipaddress': route.ipaddress,
                    'servernameEN': route.servernameEN,
                    'servernameCN': route.servernameCN,
                    'routeStarttime': route.routeStarttime,
                    'trafficLimit': route.trafficLimit,
                    'trafficUsed': route.trafficUsed,
                    'trafficResetDay': route.trafficResetDay,
                    'password':thunderservice_password
                })

            return {
                "code":200,
                "message":"login success",
                "results":{
                    "user":{
                        "user_id":user.id,
                        "thunderservice_id":user.thunderservice_id,
                        "thunderservice_endtime":user.thunderservice_endtime,
                        "usergroup_id":user.usergroup_id
                    },
                    "routes":routes_info,
                    "credential":{
                        "token" : token.decode('UTF-8'),
                        "refreshToken":refreshToken.decode('UTF-8')
                    }
                }
            }

        return {
            "code":4002,
            "message": returncode['4002'],
        },401



    def check_registed_user_by_email(self,user_email):
        if UserService.get_user_by_email(user_email):
            return True