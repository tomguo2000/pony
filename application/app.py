#!/usr/bin/env python3

import logging
import connexion
import os
from application.common.foundation import db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from application.models.user_model import UserModel
from application.models.pwresources_model import PWResourcesModel
from application.models.route_model import RouteModel
from application.models.thunderservice_model import ThunderserviceModel
from application.models.usergroup_model import UserGroupModel


def create_app():
    app = connexion.FlaskApp(__name__, specification_dir='../openapi/')
    app.add_api("api.yaml")
    load_config(app.app)
    configure_foundations(app.app)
    return app


def configure_foundations(app):
    db.app = app
    db.init_app(app)



def load_config(app):
    app.config.from_object('config.settings')

    config_file = 'config.local'

    if os.path.exists(config_file):
        app.config.from_object(config_file)


app = create_app()
flask_app = app.app
load_config(app.app)
admin = Admin(app.app)


admin.add_view(ModelView(UserModel, db.session))
admin.add_view(ModelView(PWResourcesModel, db.session))
admin.add_view(ModelView(RouteModel, db.session))
admin.add_view(ModelView(ThunderserviceModel, db.session))
admin.add_view(ModelView(UserGroupModel, db.session))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(port=8080,debug=True)
