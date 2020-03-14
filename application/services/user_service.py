from .base_service import BaseService
from application.models.user_model import UserModel
from application.common.foundation import db

class UserService(BaseService):
    @staticmethod
    def get_user(user_id):
        user = UserModel.query.filter(UserModel.id == user_id).first()
        return user.__dict__ if user else None

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

    @staticmethod
    def modify_user(user_name,user_email):
        update = UserModel.query.filter(UserModel.email == user_email).first()
        update.name = user_name
