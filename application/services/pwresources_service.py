import time
from .base_service import BaseService
from application.models.pwresources_model import PWResourcesModel

class pwresourcesService(BaseService):
    @staticmethod
    def get_pwres_by_usergroupID(usergroup_id):
        datalist = PWResourcesModel.query.filter(PWResourcesModel.usergroup_id == usergroup_id).all()
        re = []
        for row in datalist:
            user_id = row.user_id
            if user_id == None or user_id == 0:
                user_id = ''
            re.append([row.id,user_id,row.hashedpassword,row.quota,0,0])
        return re if datalist else '[]'