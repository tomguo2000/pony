from .base_service import BaseService
from application.models.setting_model import SettingModel
from application.common.foundation import db
import time,subprocess,os,json

class SettingService(BaseService):
    @staticmethod
    def add_setting(name,value):
        setting = SettingModel(
            name = name,
            value = value
        )
        db.session.add(setting)

    @staticmethod
    def delete_setting(setting_id):
        SettingModel.query.filter(SettingModel.id == setting_id).delete()

    @staticmethod
    def modify_setting_by_id(setting_id,update_data):
        update = SettingModel.query.filter(SettingModel.id == setting_id).first()
        for key in update_data:
            setattr(update,key,update_data[key])

    @staticmethod
    def get_setting_amount():
        settingAmount = SettingModel.query.filter().count()
        return settingAmount if settingAmount else 0

    @staticmethod
    def get_settings(pageNum,pageSize):
        settings = SettingModel.query.filter().limit(pageSize).offset((pageNum-1)*pageSize)
        return settings

    @staticmethod
    def get_setting(setting_id):
        setting = SettingModel.query.filter(SettingModel.id == setting_id).first()
        return setting if setting else None

    def update_status_by_name(setting):
        print ('doing update_status_by_name ')
        if setting.name == "mainserver":
            value = setting.value
            url = setting.additional
            # ping checking
            result = {}
            re_ping = subprocess.call("ping -c 3 %s" % url, shell=True,stdout=open('ping.temp','w'))
            if re_ping == 0:
                result['connection'] = "connection OK"
            else:
                result['connection']  = "connection error"

            # getCertExpDate
            os.system('openssl s_client -connect '+url+':443 < /dev/null 2> /dev/null|openssl x509 -text 2> /dev/null| grep "Not After"|sed -e "s/^ *//g"| cut -d " " -f 4,5,6,7,8 > sss.tmp')
            with open ("sss.tmp", "r") as f:
                temp = f.readline()
                expdate = temp.strip()
            result['certExpDate'] = expdate
            setting.status = json.dumps(result)
            setting.timestamp = int(time.time())
            db.session.commit()
            return True

