from .base_service import BaseService
from application.models.user_model import UserModel
from application.models.thunderservice_model import ThunderserviceModel
from application.models.pwresources_model import PWResourcesModel
from application.models.order_model import OrderModel
from application.common.foundation import db
from sqlalchemy import between,desc
import logging


class UserService(BaseService):
    @staticmethod
    def get_user_amount():
        userAmount = UserModel.query.filter().count()
        return userAmount if userAmount else 0

    @staticmethod
    def get_newuser_amount(start,end):
        userAmount = UserModel.query.filter(between(UserModel.register_datetime,start*1000,end*1000)).count()
        return userAmount if userAmount else 0

    @staticmethod
    def get_user(user_id):
        user = UserModel.query.filter(UserModel.id == user_id).first()
        return user if user else None

    @staticmethod
    def get_user_afflist(user_id):
        user = UserModel.query.filter(UserModel.mentor == user_id).all()
        return user if user else None

    @staticmethod
    def get_user_service_password(user_id):
        user_service_password = PWResourcesModel.query.filter(PWResourcesModel.user_id == user_id).first()
        return user_service_password if user_service_password else None

    @staticmethod
    def get_user_order(user_id):
        user_order = OrderModel.query.filter(OrderModel.user_id == user_id).all()
        return user_order if user_order else None

    @staticmethod
    def get_users(pageNum,pageSize):
        # users = UserModel.query.filter().limit(pageSize).offset((pageNum-1)*pageSize)
        users = db.session.query(UserModel,ThunderserviceModel).join(ThunderserviceModel, UserModel.thunderservice_id==ThunderserviceModel.id).filter().limit(pageSize).offset((pageNum-1)*pageSize)
        return users

    @staticmethod
    def get_user_by_email(checking_email):
        user = UserModel.query.filter(UserModel.email == checking_email).first()
        return user if user else None

    @staticmethod
    def user_pwdreset_submit(user_id,newpassword):
        user = UserModel.query.filter(UserModel.id == user_id).first()
        user.password = newpassword
        user.set_password(user.password)
        return True

    @staticmethod
    def add_user(user_name,user_email,user_password,register_source,email_verified,register_datetime):
        from application.common.dict import thunder_service_ID
        from application.models.thunderservice_model import ThunderserviceModel
        thunderservice = ThunderserviceModel.query.filter(ThunderserviceModel.id == thunder_service_ID["LOW_SPEED"]).first()
        thunderservice_client_amount = thunderservice.defaultClientAmount
        thunderservice_traffic_amount = thunderservice.defaultTrafficAmount
        user = UserModel(
            name = user_name,
            email = user_email,
            password = user_password,
            email_verified = email_verified,
            account_status = "ACCOUNT_ACTIVED",
            register_datetime = register_datetime,
            register_source = register_source,
            thunderservice_id = thunder_service_ID["LOW_SPEED"],
            thunderservice_client_amount = thunderservice_client_amount,
            thunderservice_traffic_amount = thunderservice_traffic_amount,
            thunderservice_starttime = register_datetime,
            thunderservice_endtime = 4102329590,
            affiliate = False
        )
        user.set_password(user.password)
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
        PWResourcesModel.query.filter(PWResourcesModel.user_id == user_id).delete()

    @staticmethod
    def assign_new_pwd(user_id,usergroup_id):
        pwd_data = PWResourcesModel.query.filter(PWResourcesModel.usergroup_id == usergroup_id).filter(PWResourcesModel.user_id == None).first()
        pwd_data.user_id = user_id

    @staticmethod
    def save_token(user_id,token,refreshToken):
        user = UserModel.query.filter(UserModel.id == user_id).first()
        user.token = token
        user.refreshToken = refreshToken

    @staticmethod
    def active_thunderservice(user_id,thunderservice_id,thunderservice_starttime,thunderservice_endtime):
        from application.models.usergroup_model import UserGroupModel
        from application.models.pwresources_model import PWResourcesModel
        from application.services.usergroup_service import UserGroupService

        logging.info ("active thunderservice: userid={},thunderservice_id={},thunderservice_starttime={},thunderservice_endtime={}".format(user_id,thunderservice_id,thunderservice_starttime,thunderservice_endtime))
        #Step1：按照已经分配的thunderservice找到可用的usergroup（usergroup的assined没有满）
        usergroups = UserGroupModel.query.filter(UserGroupModel.maxUserCapacity>UserGroupModel.current_used).all()
        available=[]
        for row in usergroups:
            if str(thunderservice_id) in (row.which_thunderservice.split(",")):
                temp = [row.current_used / row.maxUserCapacity, row.id]
                available.append(temp)
        available.sort()
        usergroup = available[0][1]

        #Step2：密码表里，把第一条可用的密码和usergroup记录中，写入userid
        data = PWResourcesModel.query.filter(PWResourcesModel.usergroup_id == usergroup , PWResourcesModel.user_id == None).first()
        data.user_id = user_id

        #Step3：usergroup表里的已分配数+1
        UserGroupService.increase(usergroup)

        #Step4：user表里写入分配的usergroup,thunderservice_starttime,thunderservice_endtime
        user = UserModel.query.filter(UserModel.id == user_id).first()
        user.usergroup_id = usergroup
        user.thunderservice_starttime = thunderservice_starttime+1
        user.thunderservice_endtime = thunderservice_endtime+1
