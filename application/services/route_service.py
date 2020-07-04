from .base_service import BaseService
from application.models.route_model import RouteModel
from application.common.foundation import db

class RouteService(BaseService):
    @staticmethod
    def get_route(route_id):
        route = RouteModel.query.filter(RouteModel.id == route_id).first()
        return route.__dict__ if route else None

    @staticmethod
    def get_routes():
        routes = RouteModel.query.all()
        routes_info = list()
        for route in routes:
            routes_info.append({
                'id': route.id,
                'group_id': route.usergroup_id,
                'sequence': route.sequence,
                'online': route.online,
                'domain': route.domain,
                'ipaddress': route.ipaddress,
                'servernameEN': route.servernameEN,
                'servernameCN': route.servernameCN,
                'routeStarttime': route.routeStarttime,
                'trafficLimit': route.trafficLimit,
                'trafficUsed': route.trafficUsed,
                'trafficResetDay': route.trafficResetDay
            })
        return routes_info

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
        #         'routeStarttime': route.routeStarttime,
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

