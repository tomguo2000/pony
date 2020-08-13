import time,calendar
from .base_service import BaseService
from application.models.usergroup_model import UserGroupModel
from application.models.route_model import RouteModel
from application.common.foundation import db

class RouteService(BaseService):
    @staticmethod
    def get_route_amount(usergroup_ids):
        if usergroup_ids == []:
            routeAmount = RouteModel.query.filter().count()
        else:
            routeAmount = RouteModel.query.filter(RouteModel.usergroup_id.in_(usergroup_ids)).count()
        return routeAmount if routeAmount else 0

    @staticmethod
    def get_route(route_id):
        route = RouteModel.query.filter(RouteModel.id == route_id).first()
        return route.__dict__ if route else None

    @staticmethod
    def get_route_class(route_id):
        route = RouteModel.query.filter(RouteModel.id == route_id).first()
        return route if route else None

    @staticmethod
    def get_route_by_ip(route_ip):
        route = RouteModel.query.filter(RouteModel.ipaddress == route_ip).first()
        return route.__dict__ if route else None

    @staticmethod
    def update_route_dynamic_data(data):
        from application.models.route_model import CpuIOModel,DiskIOModel,LoadAverageModel,NetworkModel,OnlineUserAmountModel

        route = RouteModel.query.filter(RouteModel.ipaddress == data["ipaddress"]).first()
        route.availablePwd = data["availablePwd"]

        cpu = CpuIOModel()
        cpu.ipaddress = data["ipaddress"]
        cpu.cpu = data['cpuPercent']
        cpu.mem = data['memoryPercent']
        cpu.addtime = data['timestamp']
        db.session.add(cpu)

        disk = DiskIOModel()
        disk.ipaddress = data["ipaddress"]
        disk.read_count = data["diskReadCount"]
        disk.write_count = data["diskWriteCount"]
        disk.read_bytes = data["diskReadBytes"]
        disk.write_bytes = data["diskWriteBytes"]
        disk.read_time = data["diskReadTime"]
        disk.write_time = data["diskWriteTime"]
        disk.addtime = data['timestamp']
        db.session.add(disk)

        loadaver = LoadAverageModel()
        loadaver.ipaddress = data["ipaddress"]
        loadaver.one = data["laOne"]
        loadaver.five = data["laFive"]
        loadaver.fifteen = data["laFifteen"]
        loadaver.addtime = data["timestamp"]
        db.session.add(loadaver)

        networkPrevious = NetworkModel.query.filter(NetworkModel.ipaddress == data["ipaddress"]). \
            order_by(NetworkModel.addtime.desc()).first()
        network = NetworkModel()
        network.ipaddress = data["ipaddress"]
        network.up = data["netBytesRecv"]
        network.down = data["netBytesSent"]

        if networkPrevious and network.down < networkPrevious.down:   #if server restart
            route.trafficStartAt = -route.trafficUsed

        if data["timestamp"] < route.trafficResetDay:
            route.trafficUsed = network.down - route.trafficStartAt
        else:                           #Reset to 0 when get to trafficResetDay
            struct_time = time.localtime(route.trafficResetDay)
            days = calendar.monthrange(struct_time.tm_year,struct_time.tm_mon)[1]
            route.trafficResetDay += days*24*3600
            route.trafficStartAt = network.down
            route.trafficUsed = network.down - route.trafficStartAt
        # network.total_up
        # network.total_down
        network.up_packets = data["netPacketsRecv"]
        network.down_packets = data["netPacketsSent"]
        network.addtime = data["timestamp"]
        db.session.add(network)

        onlineuser = OnlineUserAmountModel()
        onlineuser.ipaddress = data["ipaddress"]
        onlineuser.online_user_amount = data["onlineUserAmount"]
        onlineuser.server_local_time = data["localTime"]
        onlineuser.server_start_time = data["startTime"]
        onlineuser.addtime = data["timestamp"]
        db.session.add(onlineuser)




    @staticmethod
    def get_route_dynamic_data(ipaddress):
        from application.models.route_model import CpuIOModel,DiskIOModel,LoadAverageModel,NetworkModel,OnlineUserAmountModel
        dynamic_data={}
        cpu = CpuIOModel.query.filter(CpuIOModel.ipaddress == ipaddress). \
            order_by(CpuIOModel.addtime.desc()).first()
        Disk = DiskIOModel.query.filter(DiskIOModel.ipaddress == ipaddress). \
            order_by(DiskIOModel.addtime.desc()).first()
        LoadAverage = LoadAverageModel.query.filter(LoadAverageModel.ipaddress == ipaddress). \
            order_by(LoadAverageModel.addtime.desc()).first()
        Network = NetworkModel.query.filter(NetworkModel.ipaddress == ipaddress). \
            order_by(NetworkModel.addtime.desc()).first()
        OnlineUserAmount = OnlineUserAmountModel.query.filter(OnlineUserAmountModel.ipaddress == ipaddress). \
            order_by(OnlineUserAmountModel.addtime.desc()).first()

        if cpu:
            dynamic_data["cpu_persent"] = cpu.cpu
            dynamic_data["mem_persent"] = cpu.mem
        if Disk:
            dynamic_data["disk_read_count"] = Disk.read_count
            dynamic_data["disk_write_count"] = Disk.write_count
            dynamic_data["disk_read_time"] = Disk.read_time
            dynamic_data["disk_write_time"] = Disk.write_time
        if LoadAverage:
            dynamic_data["loadaverage_one"] = LoadAverage.one
            dynamic_data["loadaverage_five"] = LoadAverage.five
            dynamic_data["loadaverage_fifteen"] = LoadAverage.fifteen
        if Network:
            dynamic_data["network_total"] = Network.total_down
        if OnlineUserAmount:
            dynamic_data["online_user_amount"] = OnlineUserAmount.online_user_amount
            dynamic_data["server_local_time"] = OnlineUserAmount.server_local_time
            dynamic_data["server_start_time"] = OnlineUserAmount.server_start_time
            dynamic_data["data_checking_time"] = OnlineUserAmount.addtime

        return dynamic_data if dynamic_data else None

    @staticmethod
    def get_routes(usergroup_ids,pageNum,pageSize):
        if usergroup_ids == []:
            pass
            # routes = RouteModel.query.filter().limit(pageSize).offset((pageNum-1)*pageSize)
            routes = db.session.query(RouteModel,UserGroupModel).join(UserGroupModel,RouteModel.usergroup_id == UserGroupModel.id).\
                filter().limit(pageSize).offset((pageNum-1)*pageSize)
        else:
            # routes = RouteModel.query.filter(RouteModel.usergroup_id.in_(usergroup_ids)).limit(pageSize).offset((pageNum-1)*pageSize)
            routes = db.session.query(RouteModel,UserGroupModel).join(UserGroupModel,RouteModel.usergroup_id == UserGroupModel.id). \
                filter(RouteModel.usergroup_id.in_(usergroup_ids)).limit(pageSize).offset((pageNum-1)*pageSize)

        return routes

    @staticmethod
    def get_routes_by_group_ID(group_id):
        routes = RouteModel.query.filter(RouteModel.usergroup_id == group_id).all()
        return routes
        # routes_info = list()
        # for route in routes:
        #     routes_info.append({
        #         'id': route.id,
        #         'group_id': route.usergroup_id,
        #         'sequence': route.sequence,
        #         'online': route.online,
        #         'domain': route.domain,
        #         'ipaddress': route.ipaddress,
        #         'servernameEN': route.servernameEN,
        #         'servernameCN': route.servernameCN,
        #         'routeStartTime': route.routeStartTime,
        #         'trafficLimit': route.trafficLimit,
        #         'trafficUsed': route.trafficUsed,
        #         'trafficResetDay': route.trafficResetDay
        #     })
        # return routes_info

    @staticmethod
    def add_route(route_data):
        route=RouteModel()
        for key in route_data:
            setattr(route,key,route_data[key])
        db.session.add(route)

    @staticmethod
    def modify_route_by_id(route_id,update_data):
        update = RouteModel.query.filter(RouteModel.id == route_id).first()
        for key in update_data:
            setattr(update,key,update_data[key])

    @staticmethod
    def delete_route(route_id):
        RouteModel.query.filter(RouteModel.id == route_id).delete()

    @staticmethod
    def push_route(route_id):
        pass
        return {
            "result": "Push to route "+str(route_id)+" success"
        }

