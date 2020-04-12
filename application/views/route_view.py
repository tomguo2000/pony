from .base_view import BaseView
from application.services.route_service import RouteService
from application.common.foundation import db




"""
each class is for one API
"""


class GetRoutesView(BaseView):

    def process(self):
        self.other_function()
        routes = RouteService.get_routes()
        return routes

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
                'id': route_info.get('id'),
                'group_id': route_info.get('group_id'),
                'sequence': route_info.get('sequence'),
                'online': route_info.get('online'),
                'domain': route_info.get('domain'),
                'ipaddress': route_info.get('ipaddress'),
                'servernameEN': route_info.get('servernameEN'),
                'servernameCN': route_info.get('servernameCN'),
                'routeStarttime': route_info.get('routeStarttime'),
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
                return "Id can not be modify",400
            RouteService.modify_route_by_id(route_id,route_body)
            db.session.commit()
            return "modify user group success"
        else:
            return "user group not exist",400


class AddRouteView(BaseView):

    def process(self):
        route_body = self.parameters.get('body')

        if RouteService.get_route(route_body.get('group_id')):
            return "This group_id already used",400

        RouteService.add_route(route_body)
        db.session.commit()
        return {
            'result':"success"
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