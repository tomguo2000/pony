from .base_view import BaseView
from application.services.route_service import RouteService
from application.common.foundation import db
from application.common.returncode import returncode
from flask import request
import logging




"""
each class is for one API
"""


class GetRoutesView(BaseView):
    def process(self):
        pageNum = request.args.get('pageNum', 1, type=int)
        pageSize = request.args.get('pageSize', 10, type=int)
        usergroup_ids_str = request.args.get('usergroup',"",type =str)
        logging.info("GetRoutesView. pageNum:{},pageSize:{},usergroup_ids:{}".format(pageNum, pageSize, usergroup_ids_str))

        temp1 = usergroup_ids_str.split(',')
        usergroup_ids_list = []
        for temp in temp1:
            if temp >='0' and  temp <= '9999999':
                usergroup_ids_list.append(int(temp))

        totals = RouteService.get_route_amount(usergroup_ids_list)
        totalPages = (totals + pageSize - 1) // pageSize
        self.other_function()
        routes = RouteService.get_routes(usergroup_ids_list,pageNum,pageSize)

        routes_info = []
        for route in routes:
            routes_info.append({
                'id': route.RouteModel.id,
                'usergroup_id': route.RouteModel.usergroup_id,
                'group_name': route.UserGroupModel.group_name,
                'servernameCN': route.RouteModel.servernameCN,
                'domain': route.RouteModel.domain,
                'certificateExpTime': route.RouteModel.certificateExpTime,
                'ipaddress': route.RouteModel.ipaddress,
                'ipv6': route.RouteModel.ipv6,
                'trojanVersion': route.RouteModel.trojanVersion,
                'onlineUserAmount': route.RouteModel.onlineUserAmount,
                'current_used': route.UserGroupModel.current_used,
                'maxUserCapacity': route.UserGroupModel.maxUserCapacity,
                'maxPwdCapacity': route.UserGroupModel.maxPwdCapacity,
                'trafficUsed': route.RouteModel.trafficUsed,
                'trafficLimit': route.RouteModel.trafficLimit,
                'trafficResetDay': route.RouteModel.trafficResetDay,
                'sequence': route.RouteModel.sequence,
                'online': route.RouteModel.online,
                'lastCheckTime': route.RouteModel.lastCheckTime,
            })

        return {
            "code":200,
            "message":"get routes success",
            "results":{
                "total":totals,
                "totalPages":totalPages,
                "list":routes_info
            }
        }

    def other_function(self):
        pass

class GetRoutesByGroupIDView(BaseView):
    def process(self):
        self.other_function()
        group_id = self.parameters.get('group_id')
        routes = RouteService.get_routes_by_group_ID(group_id)
        return routes

    def other_function(self):
        pass

class GetRouteView(BaseView):
    def process(self):
        self.other_function()
        route_id = self.parameters.get('route_id')
        route_info = RouteService.get_route(route_id)
        if (route_info):
            return{
                "code":200,
                "message":"Get route success",
                "results":{
                    'id': route_info.get('id'),
                    'usergroup_id': route_info.get('usergroup_id'),
                    'domain': route_info.get('domain'),
                    'ipaddress': route_info.get('ipaddress'),
                    'ipv6': route_info.get('ipv6'),
                    'port': route_info.get('port'),
                    'online': route_info.get('online'),
                    'servernameCN': route_info.get('servernameCN'),
                    'servernameEN': route_info.get('servernameEN'),
                    'sequence': route_info.get('sequence'),
                    'trafficLimit': route_info.get('trafficLimit'),
                    'routeExpTime': route_info.get('routeExpTime'),
                    'trafficResetDay': route_info.get('trafficResetDay')
                }
            }

        else:
            return "None",400

    def other_function(self):
        pass

class DeleteRouteView(BaseView):
    def process(self):
        route_id = self.parameters.get('route_id')
        route_data = RouteService.get_route(route_id)
        if route_data:
            RouteService.delete_route(route_id)
            db.session.commit()
            return "delete success"
        else:
            return "group id not exist!",404

class ModifyRouteView(BaseView):
    def process(self):
        route_body = self.parameters.get('body')
        route_id = self.parameters.get('route_id')
        route_current_data = RouteService.get_route(route_id)
        if route_current_data:
            if route_body.get('id'):
                return {
                    "code":4012,
                    "message": returncode['4012']
                },400
            RouteService.modify_route_by_id(route_id,route_body)
            db.session.commit()
            return {
                "code":200,
                "message":"Modify route success"
            }
        else:
            return {
                "code":4017,
                "message":returncode['4017']
            },400


class AddRouteView(BaseView):

    def process(self):
        route_body = self.parameters.get('body')

        # if RouteService.get_route(route_body.get('usergroup_id')):
        #     return "This usergroup_id already used",400

        RouteService.add_route(route_body)
        db.session.commit()
        return {
            "code":200,
            "message":"Add new route success"
        }

class PushRouteView(BaseView):
    def process(self):
        route_id = self.parameters.get('route_id')
        route_data = RouteService.get_route(route_id)
        if route_data:
            RouteService.push_route(route_id)
            return "Push to route success"
        else:
            return "route not exist",400

class DynamicRouteView(BaseView):
    def process(self):
        route_id = self.parameters.get('route_id')
        route_data = RouteService.get_route(route_id)
        if route_data:
            pass
            return {
                "code":200,
                "message":"Get dynamic route data success",
                "results":"TBD"
            }
        else:
            return {
                       "code":4017,
                       "message":returncode['4017']
                   },400

class RouteRemoteControl(BaseView):
    def process(self):
        commandList = ['reboot','checkTrojanVer','refreshCert']
        route_body = self.parameters.get('body')
        print(route_body)
        route_info = RouteService.get_route(route_body.get('route_id'))
        print (route_info)

        if not route_info:
            return {
                "code":4017,
                "message":returncode['4017']
            },400
        if route_body.get('command') not in commandList:
            return {
               "code":4018,
               "message":returncode['4018']
            },400
        pass
        if self.remotecontrol(route_info.get('ipaddress') ,route_body.get('command')):
            return {
                "code":200,
                "message":"Remote command sent success"
            }
        else:
            return {
                       "code":4019,
                       "message":returncode['4019']
            },400
    def remotecontrol(self,ipaddress,command):
        import socket,time,json
        print(ipaddress,command)
        message = json.dumps({"command":command})
        TCP_PORT =8000
        BUFFER_SIZE = 1024
        try:
            # timestamp=int(time.time())
            # SIGN= hashlib.md5((newIP+str(timestamp)+RESKEY).encode(encoding='UTF-8')).hexdigest()
            # body = {"newIP": newIP, "timestamp":timestamp,"sign": SIGN}
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5.0)
            s.connect((ipaddress, TCP_PORT))
            s.send(message.encode())
            data = s.recv(BUFFER_SIZE)
            print(data)
            s.close()
            return True
        except:
            print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' ' +'Sending remotecontrol command error')
            return False
