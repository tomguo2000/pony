from .base_view import BaseView
from application.services.user_service import UserService

"""
each class is for one API
"""


class GetUserView(BaseView):

    def process(self):
        self.other_function()
        user_id = self.parameters.get('user_id')
        user_info = UserService.get_user(user_id)
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

    def other_function(self):
        pass


class DeleteUserView(BaseView):

    def process(self):
        return "success"
