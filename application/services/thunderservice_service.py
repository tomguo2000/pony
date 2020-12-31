from .base_service import BaseService
from application.models.thunderservice_model import ThunderserviceModel
from application.common.foundation import db
from application.common.dict import thunder_service_for_expressorderID
import time,json


class GetThunderservice(BaseService):
    @staticmethod
    def get_thunderservice(thunderservice_id):
        thunderservice = ThunderserviceModel.query.filter(ThunderserviceModel.id == thunderservice_id).first()
        return thunderservice if thunderservice else None

    @staticmethod
    def get_fufei_thunderservice():
        thunderserviceFufeiList = ThunderserviceModel.query.filter(ThunderserviceModel.id.in_(thunder_service_for_expressorderID['FUFEI'])).all()
        return thunderserviceFufeiList if thunderserviceFufeiList else None

