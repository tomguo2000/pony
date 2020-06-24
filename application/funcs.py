from flask import request
from functools import wraps
import jwt
from application.models.user_model import UserModel
from application.common.returncode import returncode
import config.settings

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return {
                       "code":4003,
                       "message": returncode['4003'],
                       "data":{}
                   },401

        try:
            data = jwt.decode(token, config.settings.SECRET_KEY)
            current_user = UserModel.query.filter(UserModel.id == data['user_id']).first()
        except:
            return {
                       "code":4004,
                       "message": returncode['4004'],
                       "data":{}
                   },401

        if current_user.token != token:
            return {
                       "code":4005,
                       "message": returncode['4005'],
                       "data":{}
                   },401

        return f(current_user, *args, **kwargs)

    return decorated

@token_required
def get_user(current_user,user_id, flag):
    if (not current_user.admin and current_user.id != user_id) : #既不是admin，也不是用户自己，则401
        return {
                   "code":4006,
                   "message": returncode['4006'],
                   "data":{}
               },401
    from application.views.user_view import GetUserView
    return GetUserView(locals()).as_view()

@token_required
def get_user_service(current_user,user_id, flag):
    from application.views.user_view import GetUserServiceView
    return GetUserServiceView(locals()).as_view()

def active_user_service(body, flag):
    from application.views.user_view import ActiveUserServiceView
    return ActiveUserServiceView(locals()).as_view()

@token_required
def get_users(current_user):
    if not current_user or not current_user.admin:
        return {
                   "code":4007,
                   "message": returncode['4007'],
                   "data":{}
               },401
    from application.views.user_view import GetUsersView
    return GetUsersView(locals()).as_view()

def delete_user(user_id, flag):
    from application.views.user_view import DeleteUserView
    return DeleteUserView(locals()).as_view()

def modify_user_by_id(user_id,body):
    from application.views.user_view import ModifyUserViewByID
    return ModifyUserViewByID(locals()).as_view()

def user_login(body):
    from application.views.user_view import UserLoginView
    return UserLoginView(locals()).as_view()

@token_required
def add_user(current_user,body):
    if not current_user or not current_user.admin:   #只有admin可以操作
        return {
                    "code":4007,
                   "message": returncode['4007'],
                    "businessObj":{}
               },401
    from application.views.user_view import AddUserView
    return AddUserView(locals()).as_view()

def init():
    from application.models.user_model import UserModel
    from application.common.foundation import db
    import time
    user = UserModel(
        name = 'admin',
        email = 'admin@thunder.com',
        admin = True,
        password = 'admin',
        email_verified = True,
        account_status = "ACCOUNT_ACTIVED",
        register_source = 'INIT',
        register_datetime = time.time()
    )
    user.set_password(user.password)
    db.session.add(user)
    db.session.commit()
    return {
        "message":"init success"
    }


def get_usergroup(usergroup_id, flag):
    from application.views.usergroup_view import GetUserGroupView
    return GetUserGroupView(locals()).as_view()

def get_all_usergroup():
    from application.views.usergroup_view import GetAllUserGroupView
    return GetAllUserGroupView(locals()).as_view()

def modify_usergroup_by_id(usergroup_id, body):
    from application.views.usergroup_view import ModifyUserGroupView
    return ModifyUserGroupView(locals()).as_view()

def delete_usergroup(usergroup_id, flag):
    from application.views.usergroup_view import DeleteUserGroupView
    return DeleteUserGroupView(locals()).as_view()

def add_usergroup(body):
    from application.views.usergroup_view import AddUserGroupView
    return AddUserGroupView(locals()).as_view()


def refill(usergroup_id, flag):
    from application.views.usergroup_view import RefillUserGroupView
    return RefillUserGroupView(locals()).as_view()

def add_route(body):
    from application.views.route_view import AddRouteView
    return AddRouteView(locals()).as_view()

def delete_route(route_id, flag):
    from application.views.route_view import DeleteRouteView
    return DeleteRouteView(locals()).as_view()

def modify_route_by_id(route_id,body):
    from application.views.route_view import ModifyRouteView
    return ModifyRouteView(locals()).as_view()

def get_route(route_id, flag):
    from application.views.route_view import GetRouteView
    return GetRouteView(locals()).as_view()

def get_routes():
    from application.views.route_view import GetRoutesView
    return GetRoutesView(locals()).as_view()

def get_routes_by_group_id(group_id):
    from application.views.route_view import GetRoutesByGroupIDView
    return GetRoutesByGroupIDView(locals()).as_view()

def push_route(route_id, flag):
    from application.views.route_view import PushRouteView
    return PushRouteView(locals()).as_view()