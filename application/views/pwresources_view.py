from .base_view import BaseView
from application.services.pwresources_service import pwresourcesService
from flask import request
import hashlib,time
import logging
import config.settings



"""
each class is for one API
"""

class GetPwresourcesView(BaseView):
    def process(self):
        _body = self.parameters.get('body')

        if abs(int(time.time()) - _body.get('timestamp')) > 900:
            return {"result":'error',"resource":'Fuckoff,you are toooo late'}, 200

        if not (_body.get('resgroup') and _body.get('timestamp') and _body.get('sign')):
            return {"result":'error',"resource":'Fuckoff,you are missing something'}, 200

        if not self.check_sign(_body.get('resgroup'),_body.get('timestamp'),_body.get('sign')):
            return {"result":'error',"resource":'Fuckoff,your sign is False'}, 200

        logging.info("a new requirment received:"+str(_body))

        print ("sign True")
        if ( _body.get('resgroup')[0:5] == 'fufei'):
            usergroup_id1 = int(_body.get('resgroup')[-1:])
            usergroup_id2 = usergroup_id1+100

            data1 = pwresourcesService.get_pwres_by_usergroupID(usergroup_id1)
            data2 = pwresourcesService.get_pwres_by_usergroupID(usergroup_id2)

            dataall = data1+data2

            return {"result":'success',"resgroup":_body.get('resgroup'),"resource":dataall}, 200





    def check_sign(self,arg1, arg2, arg3):
        x = hashlib.md5((arg1+str(arg2)+config.settings.ROUTE_KEY).encode(encoding='UTF-8')).hexdigest()
        if (x == arg3):
            return True
        else:
            return False
