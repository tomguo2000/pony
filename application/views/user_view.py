from .base_view import BaseView
from application.services.user_service import UserService
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
        if UserService.get_user(user_id):
            UserService.modify_user_by_id(user_id,user_body)
            db.session.commit()
            return "modify user success"
        else:
            return "user not exist",400

class ModifyUserView(BaseView):

    def process(self):
        user_body = self.parameters.get('body')
        if UserService.get_user_by_email(user_body.get('email')):
            #body里传入email和任意字段，怎么写任意字段的修改
            UserService.modify_user(user_body.get('name'),user_body.get('email'))
            db.session.commit()
            return "modify user success"
        else:
            return "user not exist",400

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