from .base_view import BaseView
from application.services.usergroup_service import UserGroupService
from application.common.foundation import db
import logging
logger = logging.getLogger(__name__)



"""
each class is for one API
"""


class GetAllUserGroupView(BaseView):

    def process(self):
        self.other_function()
        usergroup_ids = [0]
        rows = UserGroupService.get_allusergroup()
        for (usergroup_id) in rows:
            usergroup_ids.append(usergroup_id)

        #print (usergroup_ids)
        return usergroup_ids

        # return {
        #     'group_id': usergroup_info.get('id'),
        #     'group_name': usergroup_info.get('group_name'),
        #     'maxcapacity': usergroup_info.get('maxcapacity'),
        #     'current_capacity': usergroup_info.get('current_capacity'),
        #     'trojan_password': usergroup_info.get('trojan_password'),
        #     'trojan_password_sha': usergroup_info.get('trojan_password_sha'),
        #     'assigned': usergroup_info.get('assigned')
        # }

    def other_function(self):
        pass


class GetUserGroupView(BaseView):

    def process(self):
        self.other_function()
        usergroup_id = self.parameters.get('user_group_id')
        usergroup_info = UserGroupService.get_usergroup(usergroup_id)

        if (usergroup_info):
            return {
                'id': usergroup_info.get('id'),
                'group_id': usergroup_info.get('group_id'),
                'group_name': usergroup_info.get('group_name'),
                'maxcapacity': usergroup_info.get('maxcapacity'),
                'current_capacity': usergroup_info.get('current_capacity'),
                'trojan_password': usergroup_info.get('trojan_password'),
                'trojan_password_sha': usergroup_info.get('trojan_password_sha'),
                'assigned': usergroup_info.get('assigned')
            }
        else:
            return "None",400


    def other_function(self):
        pass


class DeleteUserGroupView(BaseView):
    def process(self):
        usergroup_id = self.parameters.get('user_group_id')
        usergroup_data = UserGroupService.get_usergroup(usergroup_id)
        if usergroup_data:
            UserGroupService.delete_usergroup(usergroup_data)
            db.session.commit()
            return "delete success"
        else:
            return "group_id not exist!",400


class ModifyUserGroupView(BaseView):
    def process(self):
        usergroup_body = self.parameters.get('body')
        usergroup_id = self.parameters.get('user_group_id')

        if UserGroupService.get_usergroup(usergroup_id):
            UserGroupService.modify_usergroup_by_id(usergroup_id,usergroup_body)
            db.session.commit()
            return "modify user group success"
        else:
            return "user group not exist",400


class AddUserGroupView(BaseView):

    def process(self):
        usergroup_body = self.parameters.get('body')

        if UserGroupService.get_usergroup(usergroup_body.get('group_id')):
            return "This group_id already used",400

        UserGroupService.add_usergroup(usergroup_body)
        db.session.commit()
        return {
            'result':"success"
        }
