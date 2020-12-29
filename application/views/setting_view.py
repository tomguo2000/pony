from .base_view import BaseView
from application.services.setting_service import SettingService
from application.common.foundation import db
import time, json, base64, random
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
        if not setting.timestamp or (int(time.time()) - setting.timestamp >60):
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

class GenMagicView(BaseView):
    def process(self):
        data = {
            "api_gateway":[
                "http://114.115.144.166:8080",
                "https://not.availablenow.com:443"
            ],
            "website_proxy":"https://not.availablenow.com:443",
            "windows_client_ver":"6.0",
            "windows_client_download_url":"https://obs-9bcf.obs.cn-north-1.myhuaweicloud.com:443/release/Thunder_Test_V5.1.2.zip",
            "android_client_ver":"2.7",
            "android_client_download_url":"https://obs-9bcf.obs.cn-north-1.myhuaweicloud.com:443/release/ThunderAcc_release_3.1_sign.apk",
            "mac_client_ver":"1.7",
            "mac_client_download_url":"https://obs-9bcf.obs.cn-north-1.myhuaweicloud.com:443/release/Trojan2021.dmg"
        }

        data = json.dumps(data)
        print (type (data))
        print (data)

        bytes = data.encode()
        encoded = base64.b64encode(bytes)
        encoded_str = encoded.decode()

        try:
            new_list = []
            i = int(len(encoded_str)/8)
            if i != 0:
                for j in range(0, i+1):
                    new_list.append(encoded_str[j*8:(j+1)*8])
                if len(new_list[-1]) == 0:
                    new_list.pop(-1)
            else:
                new_list.append(encoded_str)

            magic_list = []
            for i in range(0, len(new_list)-1):
                temp = list(new_list[i])
                temp.reverse()
                magic_list.append(''.join(temp))    #reverse every 8 character
                magic_list.append(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'))    #add random character for each section
                magic_list.append(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'))    #add random character for each section

            magic_list.append(new_list[-1])

            magic_str = ''.join(magic_list)

            return {
                "code": 200,
                "message": "Generate magic character success",
                "results": magic_str
            }

        except:
            return {
                       "code": 5002,
                       "message": returncode['5002']
                   }, 400


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
