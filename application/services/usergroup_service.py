from .base_service import BaseService
from application.models.usergroup_model import UserGroupModel
from application.models.pwresources_model import PWResourcesModel
from application.models.route_model import RouteModel
from application.common.foundation import db

class UserGroupService(BaseService):
    @staticmethod
    def get_usergroup(usergroup_id):
        usergroup = UserGroupModel.query.filter(UserGroupModel.id == usergroup_id).first()
        return usergroup.__dict__ if usergroup else None

    @staticmethod
    def get_usergroup_reality(usergroup_id):
        pwd_count = PWResourcesModel.query.filter(PWResourcesModel.group_id==usergroup_id).count()
        pwd_assigned = PWResourcesModel.query.filter(PWResourcesModel.group_id==usergroup_id).filter(PWResourcesModel.uid != None).count()
        pwd_available = PWResourcesModel.query.filter(PWResourcesModel.group_id==usergroup_id).filter(PWResourcesModel.uid == None).count()
        return {
            "pwd_count":pwd_count,
            "pwd_assigned":pwd_assigned,
            "pwd_available":pwd_available
        }

    @staticmethod
    def get_allusergroup():
        usergroups = UserGroupModel.query.all()
        results = list()
        for row in usergroups:
            results.append({
                'id':row.id,
                'group_name':row.group_name,
                'maxcapacity':row.maxcapacity,
                'current_capacity':row.current_capacity,
                'which_service':row.which_service
            })
        return results


    @staticmethod
    def add_usergroup(usergroup_data):
        usergroup = UserGroupModel()
        for key in usergroup_data:
            setattr(usergroup,key,usergroup_data[key])
        db.session.add(usergroup)

    @staticmethod
    def modify_usergroup_by_id(usergroup_id,update_data):
        update = UserGroupModel.query.filter(UserGroupModel.id == usergroup_id).first()
        for key in update_data:
            setattr(update,key,update_data[key])

    @staticmethod
    def delete_usergroup(usergroup):
        routes = RouteModel.query.filter(RouteModel.group_id == usergroup).all()
        for route in routes:
            route.group_id="None"
        UserGroupModel.query.filter(UserGroupModel.id == usergroup).delete()

    @staticmethod
    def refill(usergroup_id,refill_count):
        import random,hashlib
        objects=[]
        i=0
        while i < refill_count:
            x=random.randint(0,9999999999999999999999999999999999999999999999999999999999999999999999999999999999)
            o = hashlib.md5(str(x).encode('UTF-8'))
            oripassword = o.hexdigest().encode('UTF-8')
            h = (hashlib.sha224(oripassword))
            hashedpassword = h.hexdigest()
            objects.append(PWResourcesModel(group_id=usergroup_id, oripassword=oripassword, hashedpassword=hashedpassword))
            i+=1
        db.session.add_all(objects)


    @staticmethod
    def check_availablepassword(usergroup_id):
        total = UserGroupModel.query.filter(UserGroupModel.id==usergroup_id).count()
        available = UserGroupModel.query.filter(UserGroupModel.id==usergroup_id,UserGroupModel.uid.is_(None) ).count()
        print(total,available)
        return total,available

    @staticmethod
    def decrease(usergroup_id):
        usergroup_data = UserGroupModel.query.filter(UserGroupModel.id == usergroup_id).first()
        usergroup_data.current_capacity -=1

    @staticmethod
    def increase(usergroup_id):
        usergroup_data = UserGroupModel.query.filter(UserGroupModel.id == usergroup_id).first()
        usergroup_data.current_capacity +=1