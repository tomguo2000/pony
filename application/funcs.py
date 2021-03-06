from flask import request,render_template,make_response
from functools import wraps
import jwt,json,hashlib,time
from application.models.user_model import UserModel
from application.common.returncode import returncode
import config.settings


def app_sign_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        sign = None

        if 'sign' in request.headers:
            sign = request.headers['sign']

        if not sign:
            return {
                       "code":4026,
                       "message": returncode['4026'],
                       "data":{}
                   },401

        body = json.loads(request.get_data())
        try:

            appkey = body.get("appkey")
            timestamp = body.get("timestamp")
            timestamp = str(timestamp)
            sk = config.settings.AK_SK.get(appkey)["sk"]
            sign_oridata = appkey+timestamp+sk
            sign_oridata = sign_oridata.encode()
            print (sign_oridata)
            signed = hashlib.md5(sign_oridata).hexdigest()
            print (signed)
            if signed != sign.lower():
                return {
                           "code":4027,
                           "message": returncode['4027'],
                           "data":{}
                       },401
        except:
            return {
                       "code":4027,
                       "message": returncode['4027'],
                       "data":{}
                   },401

        if abs(body.get("timestamp") - int(time.time())) > 600:
            return {
                       "code":4028,
                       "message": returncode['4028'],
                       "data":{}
                   },401

        return f(*args, **kwargs)

    return decorated

def user_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        user_id_get =request.args.get('user_id')   #might be None

        body = (request.get_data())                #might be b''
        print (body)
        try:
            user_id_post = json.loads(body).get("user_id")
        except:
            user_id_post = None

        if user_id_get:
            user_id = user_id_get
        elif user_id_post:
            user_id = user_id_post
        else:
            return {
                       "code":5003,
                       "message": returncode['5003'],
                       "data":{}
                   },401

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

        if (not current_user.admin) and (current_user.id != int(user_id)) : #既不是admin，也不是用户自己，则401。
            return {
                       "code":4006,
                       "message": returncode['4006'],
                   },401

        # return f(current_user, *args, **kwargs)    #返回token中的userid给被装饰的函数
        return f(*args, **kwargs)
    return decorated

def admin_token_required(f):
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

        if not current_user or not current_user.admin:   #只有admin可以操作，如果token对应的账户不存在，不会出错
            return {
                       "code":4007,
                       "message": returncode['4007'],
                       "data":{}
                   },401

        return f(*args, **kwargs)

    return decorated

@user_token_required
def get_user(user_id, flag):
    from application.views.user_view import GetUserView
    return GetUserView(locals()).as_view()

@user_token_required
def get_user_order(user_id, flag):
    from application.views.user_view import GetUserOrderView
    return GetUserOrderView(locals()).as_view()

@user_token_required
def get_user_service(user_id, flag):
    from application.views.user_view import GetUserServiceView
    return GetUserServiceView(locals()).as_view()

def active_user_service(body, flag):
    from application.views.user_view import ActiveUserServiceView
    return ActiveUserServiceView(locals()).as_view()

@admin_token_required
def get_users():
    from application.views.user_view import GetUsersView
    return GetUsersView(locals()).as_view()

def delete_user(user_id, flag):
    from application.views.user_view import DeleteUserView
    return DeleteUserView(locals()).as_view()

@admin_token_required
def modify_user_by_id(user_id,body):
    from application.views.user_view import ModifyUserViewByID
    return ModifyUserViewByID(locals()).as_view()

def user_login(body):
    from application.views.user_view import UserLoginView
    return UserLoginView(locals()).as_view()

@admin_token_required
def add_user(body):
    from application.views.user_view import AddUserView
    return AddUserView(locals()).as_view()

@app_sign_required
def app_register(body):
    from application.views.app_view import AppRegisterUserView
    return AppRegisterUserView(locals()).as_view()

@app_sign_required
def app_login(body):
    from application.views.app_view import AppUserLoginView
    return AppUserLoginView(locals()).as_view()

@user_token_required
def app_get_user(user_id):
    from application.views.app_view import AppGetUserView
    return AppGetUserView(locals()).as_view()

def app_refresh_token(body):
    from application.views.app_view import AppRefreshTokenView
    return AppRefreshTokenView(locals()).as_view()

@user_token_required
def app_get_announcement(user_id):
    from application.views.app_view import AppGetAnnouncementView
    return AppGetAnnouncementView(locals()).as_view()

@user_token_required
def app_feedback(body):
    from application.views.app_view import AppFeedbackView
    return AppFeedbackView(locals()).as_view()

@user_token_required
def app_addExpressorder(body):
    from application.views.order_view import addExpressorder
    return addExpressorder(locals()).as_view()

def app_expressorder_view(orderID):
    #给手机扫码用，不带任何token
    from application.views.order_view import expressorderView
    return expressorderView(locals()).as_view()

@user_token_required
def app_checkExpressOrderResult(body):
    from application.views.order_view import appCheckExpressOrderResult
    return appCheckExpressOrderResult(locals()).as_view()

@admin_token_required
def add_order(body):
    from application.views.order_view import AddOrderView
    return AddOrderView(locals()).as_view()

@admin_token_required
def get_orders():
    from application.views.order_view import GetOrdersView
    return GetOrdersView(locals()).as_view()

@user_token_required
def get_order(order_id, flag):
    from application.views.order_view import GetOrderView
    return GetOrderView(locals()).as_view()

@admin_token_required
def fulfill_order(order_id):
    from application.views.order_view import FulfillOrderView
    return FulfillOrderView(locals()).as_view()

@admin_token_required
def mark_order_paid(order_id):
    from application.views.order_view import MarkOrderPaidView
    return MarkOrderPaidView(locals()).as_view()

@admin_token_required
def cancel_order_by_order_id(order_id):
    from application.views.order_view import CancelOrderView
    return CancelOrderView(locals()).as_view()

@admin_token_required
def delete_order(order_id):
    from application.views.order_view import DeleteOrderView
    return DeleteOrderView(locals()).as_view()



def init():
    from application.models.user_model import UserModel
    from application.models.usergroup_model import UserGroupModel
    from application.models.thunderservice_model import ThunderserviceModel
    from application.models.route_model import RouteModel
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
        register_datetime = time.time()*1000
    )
    user.set_password(user.password)
    db.session.add(user)
    db.session.commit()

    usergroup1 = UserGroupModel(
        id = 1,
        group_name = "低速线路",
        maxUserCapacity = 30,
        maxPwdCapacity = 100,
        current_used = 0,
        which_thunderservice = "1"
    )
    usergroup2 = UserGroupModel(
        id = 2,
        group_name = "TRIAL",
        maxUserCapacity = 30,
        maxPwdCapacity = 100,
        current_used = 0,
        which_thunderservice = "2"
    )
    usergroup3 = UserGroupModel(
        id = 3,
        group_name = "FUFEI1",
        maxUserCapacity = 30,
        maxPwdCapacity = 100,
        current_used = 0,
        which_thunderservice = "3,4,5"
    )
    db.session.add(usergroup1)
    db.session.add(usergroup2)
    db.session.add(usergroup3)
    db.session.commit()

    thunderservice1 = ThunderserviceModel(
        id = 1,
        membershipCN = "普通会员",
        membershipEN = "membership",
        duration = 9999,
        defaultClientAmount = 1,
        defaultTrafficAmount = -1,
        price = 0
    )
    thunderservice2 = ThunderserviceModel(
        id = 2,
        membershipCN = "体验会员",
        membershipEN = "trial",
        duration = 3,
        defaultClientAmount = 1,
        defaultTrafficAmount = -1,
        price = 0
    )
    thunderservice3 = ThunderserviceModel(
        id = 3,
        membershipCN = "银牌会员",
        membershipEN = "silver",
        duration = 31,
        defaultClientAmount = 1,
        defaultTrafficAmount = -1,
        price = 4.99
    )
    thunderservice4 = ThunderserviceModel(
        id = 4,
        membershipCN = "金牌会员",
        membershipEN = "golden",
        duration = 366,
        defaultClientAmount = 3,
        defaultTrafficAmount = -1,
        price = 49.99
    )
    thunderservice5 = ThunderserviceModel(
        id = 5,
        membershipCN = "铂金会员",
        membershipEN = "platinum",
        duration = 730,
        defaultClientAmount = 3,
        defaultTrafficAmount = -1,
        price = 89.99
    )
    db.session.add(thunderservice1)
    db.session.add(thunderservice2)
    db.session.add(thunderservice3)
    db.session.add(thunderservice4)
    db.session.add(thunderservice5)
    db.session.commit()

    route1 = RouteModel(
        id = 1,
        sequence = 1,
        online = True,
        domain = "free6.thchroute.club",
        ipaddress = "free6.thchroute.club",
        port = 443,
        servernameEN = "low_speed_route6",
        servernameCN = "低速线路6",
        routeStartTime =1593532800000,
        trafficLimit = 9000,
        trafficUsed = 0,
        trafficStartAt = 0,
        trafficResetDay = "1",
        usergroup_id = 1
    )
    route2 = RouteModel(
        id = 2,
        sequence = 1,
        online = True,
        domain = "trial.thchroute.club",
        ipaddress = "trial.thchroute.club",
        port = 443,
        servernameEN = "trial",
        servernameCN = "高速试用线路",
        routeStartTime =1593532800000,
        trafficLimit = 9000,
        trafficUsed = 0,
        trafficStartAt = 0,
        trafficResetDay = "1",
        usergroup_id = 2
    )
    route3 = RouteModel(
        id = 3,
        sequence = 1,
        online = True,
        domain = "do1n.thchroute.club",
        ipaddress = "do1n.thchroute.club",
        port = 443,
        servernameEN = "Singapore",
        servernameCN = "新加坡",
        routeStartTime =1593532800000,
        trafficLimit = 2000,
        trafficUsed = 0,
        trafficStartAt = 0,
        trafficResetDay = "1",
        usergroup_id = 3
    )
    db.session.add(route1)
    db.session.add(route2)
    db.session.add(route3)
    db.session.commit()

    return {
        "message":"init success, use /usergroups/refill/1 to refill pwresources"
    }

def search_tracking(body):
    from application.views.admin_view import searchTrackingView
    return searchTrackingView(locals()).as_view()

def get_usergroup(usergroup_id, flag):
    from application.views.usergroup_view import GetUserGroupView
    return GetUserGroupView(locals()).as_view()

def get_all_usergroup(thunderservice):
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

def route_dynamic_data(route_id, flag):
    from application.views.route_view import DynamicRouteView
    return DynamicRouteView(locals()).as_view()

def route_dynamic_dataupdate(body):
    from application.views.route_view import UpdateDynamicRouteView
    return UpdateDynamicRouteView(locals()).as_view()

def route_remotecontrol(body):
    from application.views.route_view import RouteRemoteControl
    return RouteRemoteControl(locals()).as_view()

def route_get_pwresources(body):
    from application.views.pwresources_view import GetPwresourcesView
    return GetPwresourcesView(locals()).as_view()


@admin_token_required
def gen_magic():
    from application.views.setting_view import GenMagicView
    return GenMagicView(locals()).as_view()

@admin_token_required
def add_setting(body):
    from application.views.setting_view import AddSettingView
    return AddSettingView(locals()).as_view()

@admin_token_required
def get_settings():
    from application.views.setting_view import GetSettingsView
    return GetSettingsView(locals()).as_view()

@admin_token_required
def get_setting(setting_id, flag):
    from application.views.setting_view import GetSettingView
    return GetSettingView(locals()).as_view()

@admin_token_required
def delete_setting(setting_id):
    from application.views.setting_view import DeleteSettingView
    return DeleteSettingView(locals()).as_view()

@admin_token_required
def modify_setting_by_id(setting_id,body):
    from application.views.setting_view import ModifySettingViewByID
    return ModifySettingViewByID(locals()).as_view()

@admin_token_required
def graph_online():
    from application.views.graph_view import GetOnlineView
    return GetOnlineView(locals()).as_view()

@admin_token_required
def graph_k():
    from application.views.graph_view import GetKView
    return GetKView(locals()).as_view()

@admin_token_required
def dashboard():
    from application.views.dashboard_view import GetDashboardView
    return GetDashboardView(locals()).as_view()

def pwdreset():
    from application.views.user_view import ResetPasswordView
    return ResetPasswordView(locals()).as_view()

def pwdreset_token(body):
    from application.views.user_view import PwdResetTokenView
    return PwdResetTokenView(locals()).as_view()

def expresspay(body):
    from application.views.paymentgateway_view import FinishOrderView
    return FinishOrderView(locals()).as_view()