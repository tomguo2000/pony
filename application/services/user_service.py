from .base_service import BaseService
from application.models.user_model import UserModel


class UserService(BaseService):
    @staticmethod
    def get_user(user_id):
        user = UserModel.query.filter(UserModel.id == user_id).first()
        return user.__dict__ if user else None
