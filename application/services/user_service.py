from .base_service import BaseService
from application.models.user_model import UserModel
from application.models.pwresources_model import PWResourcesModel
from application.common.foundation import db

class UserService(BaseService):
    @staticmethod
    def get_user(user_id):
        user = UserModel.query.filter(UserModel.id == user_id).first()
        return user.__dict__ if user else None


    @staticmethod
    def get_user_service_password(user_id):
        user_service_password = PWResourcesModel.query.filter(PWResourcesModel.uid == user_id).first()
        return user_service_password.__dict__ if user_service_password else None

    @staticmethod
    def get_users():
        users = UserModel.query.all()
        users_info = list()
        for user in users:
            users_info.append({
                'user_id': user.id,
                'user_name': user.name,
                'user_email': user.email,
                'user_usergroup': user.usergroup,
                'user_membership': user.membership,
                'user_membership_starttime': user.membership_starttime,
                'user_membership_endtime': user.membership_endtime
            })
        return users_info

    @staticmethod
    def get_user_by_email(checking_email):
        user = UserModel.query.filter(UserModel.email == checking_email).first()
        return user.__dict__ if user else None

    @staticmethod
    def add_user(user_name,user_email,user_password):
        user = UserModel(
            name = user_name,
            email = user_email,
            password = user_password,
        )
        db.session.add(user)
        #return user.__dict__ if user else None

    # @staticmethod
    # def modify_user(user_name,user_email):
    #     update = UserModel.query.filter(UserModel.email == user_email).first()
    #     update.name = user_name

    @staticmethod
    def modify_user_by_id(user_id,update_data):
        update = UserModel.query.filter(UserModel.id == user_id).first()
        for key in update_data:
            setattr(update,key,update_data[key])

    @staticmethod
    def delete_assigned_pwd(user_id):
        PWResourcesModel.query.filter(PWResourcesModel.uid == user_id).delete()

    @staticmethod
    def assign_new_pwd(user_id,usergroup_id):
        pwd_data = PWResourcesModel.query.filter(PWResourcesModel.group_id == usergroup_id).filter(PWResourcesModel.uid == None).first()
        pwd_data.uid = user_id
