from .base_service import BaseService
from application.models.setting_model import SettingModel
from application.common.foundation import db
import time,subprocess,os,json,requests,base64

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

    @staticmethod
    def check_proxyurl(name,url):
        result = {"name":name}
        temp = requests.get(url)
        if temp.status_code == 200:
            result['connection'] = "connection OK"
        else:
            result['connection']  = "connection error"
        if url[4] == 's':
            #it is a https url, need getCertExpDate
            url = url.split('//')[1]
            os.system('openssl s_client -connect '+url+':443 < /dev/null 2> /dev/null|openssl x509 -text 2> /dev/null| grep "Not After"|sed -e "s/^ *//g"| cut -d " " -f 4,5,6,7,8 > sss.tmp')
            with open ("sss.tmp", "r") as f:
                temp = f.readline()
                expdate = temp.strip()
            result['certExpDate'] = expdate
        else:
            result['certExpDate'] = 'N/A'
        return result

    @staticmethod
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

        if setting.name == "paymentserver":
            value = setting.value
            url = value.split('//')[1]
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

        if setting.name == "configserver":
            value = setting.value
            url = value
            data = requests.get(url)
            if data.status_code != 200:
                setting.status = json.dumps({"connection" : "connection error"})
                setting.timestamp = int(time.time())
                db.session.commit()
                return True
            else:
                setting.status = json.dumps({"connection" : "connection OK"})
                setting.timestamp = int(time.time())
                db.session.commit()
                base64data = data.text
                templist = base64.b64decode(base64data).decode("utf-8")
                templist = templist.split('\n')
                i = 0
                while i < len(templist):
                    proxyurl = (templist[i].split('url=')[1].split('|')[0])
                    temp = SettingService.check_proxyurl("proxyserver"+str(i),proxyurl)
                    proxysetting =  SettingModel.query.filter(SettingModel.name == temp['name']).first()
                    if proxysetting:
                        #this proxy name exist,update status
                        proxysetting.value = proxyurl
                        temp.pop('name')
                        proxysetting.status = json.dumps(temp)
                        proxysetting.timestamp = int(time.time())
                        db.session.commit()
                    else:
                        #this is a new proxy name, add it
                        proxysetting = SettingModel()
                        proxysetting.name = temp['name']
                        proxysetting.value = proxyurl
                        temp.pop('name')
                        proxysetting.status = json.dumps(temp)
                        proxysetting.timestamp = int(time.time())
                        db.session.add(proxysetting)
                        db.session.commit()
                    i+=1
                return True