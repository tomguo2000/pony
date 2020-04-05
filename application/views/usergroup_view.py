from .base_view import BaseView
from application.services.usergroup_service import UserGroupService
from application.common.foundation import db




"""
each class is for one API
"""


class GetAllUserGroupView(BaseView):

    def process(self):
        self.other_function()
        usergroups = UserGroupService.get_allusergroup()
        return usergroups

    def other_function(self):
        pass


class GetUserGroupView(BaseView):
    def process(self):
        self.other_function()
        usergroup_id = self.parameters.get('usergroup_id')
        usergroup_info = UserGroupService.get_usergroup(usergroup_id)
        if (usergroup_info):
            return {
                'id': usergroup_info.get('id'),
                'group_name': usergroup_info.get('group_name'),
                'maxcapacity': usergroup_info.get('maxcapacity'),
                'current_capacity': usergroup_info.get('current_capacity'),
            }
        else:
            return "None",400

    def other_function(self):
        pass

class DeleteUserGroupView(BaseView):
    def process(self):
        usergroup_id = self.parameters.get('usergroup_id')
        usergroup_data = UserGroupService.get_usergroup(usergroup_id)
        if usergroup_data:
            print (usergroup_data)
            if usergroup_data.get('current_capacity') != 0:
                return "current_capacity is not equal to zero",400
            UserGroupService.delete_usergroup(usergroup_data.get('id'))
            db.session.commit()
            return "delete success"
        else:
            return "group id not exist!",404

class ModifyUserGroupView(BaseView):
    def process(self):
        usergroup_body = self.parameters.get('body')
        usergroup_id = self.parameters.get('usergroup_id')
        usergroup_data = UserGroupService.get_usergroup(usergroup_id)
        if usergroup_data:
            if usergroup_data.get('current_capacity') > usergroup_body.get('maxcapacity'):
                return "maxcapacity too low, this usergroup already have "+str(usergroup_data.get('current_capacity'))+"users",400
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

class RefillUserGroupView(BaseView):
    def process(self):
        usergroup_id = self.parameters.get('usergroup_id')
        usergroup_data = UserGroupService.get_usergroup(usergroup_id)
        usergroup_reality = UserGroupService.get_usergroup_reality(usergroup_id)

        if usergroup_data:
            refill_count = usergroup_data.get('maxcapacity') - usergroup_reality.get('pwd_count')
            UserGroupService.refill(usergroup_id,refill_count)
            db.session.commit()
            return "user group refilled success"
        else:
            return "user group not exist",400