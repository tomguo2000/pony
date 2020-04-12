from .base_view import BaseView
from application.services.user_service import UserService
from application.services.route_service import RouteService
from application.services.usergroup_service import UserGroupService
from application.common.foundation import db

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
                'user_id': user_info.get('id'),
                'user_name': user_info.get('name'),
                'user_email': user_info.get('email'),
                'user_password': user_info.get('password11'),
                'user_usergroup': user_info.get('usergroup'),
                'user_membership': user_info.get('membership'),
                'user_membership_starttime': user_info.get('membership_starttime'),
                'user_membership_endtime': user_info.get('membership_endtime')
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
        users = UserService.get_users()
        return users

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
            return "This email already registed",400

        UserService.add_user(user_body.get('name'),user_body.get('email'),user_body.get('password'))
        db.session.commit()
        return {
            'result':"success"
        }

    def check_registed_user_by_email(self,user_email):
        if UserService.get_user_by_email(user_email):
            return True