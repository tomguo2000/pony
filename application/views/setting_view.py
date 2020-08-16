from .base_view import BaseView
from application.services.setting_service import SettingService
from application.common.foundation import db
import time,json
from application.common.returncode import returncode
from flask import request
import logging



"""
each class is for one API
"""
class GetSettingView(BaseView):
    def process(self):
        setting_id = self.parameters.get('setting_id')
        logging.info("GetSettingView. setting_id:{}".format(setting_id))
        setting = SettingService.get_setting(setting_id)
        print (setting)
        if not setting.timestamp:
            SettingService.update_status_by_name(setting)
            setting = SettingService.get_setting(setting_id)

        if int(time.time()) - setting.timestamp >60:
            SettingService.update_status_by_name(setting)
            setting = SettingService.get_setting(setting_id)

        if (setting):
            setting_info = {
                'setting_id': setting.id,
                "setting_name": setting.name,
                "setting_value" : setting.value,
                "setting_additional" : setting.additional,
                "setting_status" : json.loads(setting.status if setting.status else '{}'),
                "setting_timestamp" : setting.timestamp
            }

            return {
                "code": 200,
                "message": "get setting success",
                "results": setting_info
            }
        return {
                   "code": 4021,
                   "message": returncode['4021']
               },400

class GetSettingsView(BaseView):
    def process(self):
        pageNum = request.args.get('pageNum', 1, type=int)
        pageSize = request.args.get('pageSize', 10, type=int)
        logging.info("GetSettingsView. pageNum:{},pageSize:{}".format(pageNum, pageSize))

        totals = SettingService.get_setting_amount()
        totalPages = (totals + pageSize - 1) // pageSize
        settings = SettingService.get_settings(pageNum, pageSize)
        settingsview = list()
        for setting in settings:
            settingsview.append({
                'setting_id': setting.id,
                "setting_name": setting.name,
                "setting_value" : setting.value,
                "setting_additional" : setting.additional,
                "setting_status" : json.loads(setting.status if setting.status else '{}'),
                "setting_timestamp" : setting.timestamp
            })
        return {
            "code": 200,
            "message": "get settings success",
            "results": {
                "totals": totals,
                "totalPages": totalPages,
                "list": settingsview
            }
        }

class AddSettingView(BaseView):
    def process(self):
        data = self.parameters.get('body')
        logging.info("AddOrderView. data:{}".format(data))
        if data.get('name') and data.get('value'):
            SettingService.add_setting(data['name'],data['value'])
            db.session.commit()
            return {
                "code":200,
                "message":"Add setting success"
            }
        else:
            return {
                       "code": 4022,
                       "message": returncode['4022']
                   },400

class DeleteSettingView(BaseView):
    def process(self):
        setting_id = self.parameters.get('setting_id')
        setting_data = SettingService.get_setting(setting_id)
        if setting_data:
            SettingService.delete_setting(setting_id)
            db.session.commit()
            return{
                "code":200,
                "message":"delete success"
            }
        else:
            return{
                      "code":4021,
                      "message": returncode['4021']
                  } ,401


class ModifySettingViewByID(BaseView):
    def process(self):
        setting_body = self.parameters.get('body')
        setting_id = self.parameters.get('setting_id')
        current_settingdata = SettingService.get_setting(setting_id)
        if current_settingdata:
            if setting_body.get('id'):
                return {
                           "code": 4012,
                           "message": returncode['4012']
                       }, 400
            logging.info("ModifySettingViewByID. SettingService.modify_setting_by_id:{}{}".format(setting_id, setting_body))
            SettingService.modify_setting_by_id(setting_id,update_data=setting_body)
            db.session.commit()
            return {
                "code": 200,
                "message": "modify setting success"
            }

        else:
            return {
                       "code": 4021,
                       "message": returncode['4021']
                   }, 400
