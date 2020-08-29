from .base_service import BaseService
from application.models.usergroup_model import UserGroupModel
from application.models.pwresources_model import PWResourcesModel
from application.models.route_model import RouteModel
from application.common.foundation import db
from application.services.k_service import KService
from application.services.user_service import UserService
from application.services.order_service import OrderService
from application.services.usergroup_service import UserGroupService


class DashboardService(BaseService):
    @staticmethod
    def get_summary(thisDayStart,thisDayEnd,thisMonthStart,thisMonthEnd):
        newUserToday = UserService.get_newuser_amount(thisDayStart,thisDayEnd)
        totalUser = UserService.get_user_amount()
        membershipDAU = KService.get_user_DAU('102',thisDayStart,thisDayEnd)
        VipDAU = KService.get_user_DAU('103',thisDayStart,thisDayEnd)
        incomeDay = OrderService.get_paidOrder_sum(thisDayStart,thisDayEnd)
        incomeMonth = OrderService.get_paidOrder_sum(thisMonthStart,thisMonthEnd)
        data = {
            "newUserToday":newUserToday,
            "totalUser":totalUser,
            "membershipDAU":membershipDAU,
            "VipDAU":VipDAU,
            "incomeDay":incomeDay,
            "incomeMonth":incomeMonth
        }
        return data


    @staticmethod
    def get_allGroupsStatus():
        usergroups = UserGroupModel.query.all()
        data=[]

        for usergroup in usergroups:
            temp={}
            temp['id'] = usergroup.id
            temp['name'] = usergroup.group_name
            temp['maxUserCapacity'] = usergroup.maxUserCapacity
            temp['current_used'] = usergroup.current_used
            tempPwd = UserGroupService.get_usergroup_reality(usergroup.id)
            temp['pwd_available'] = tempPwd['pwd_available']
            temp['pwd_max'] = usergroup.maxPwdCapacity
            data.append(temp)
        return data if data else None
