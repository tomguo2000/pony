
'''
from env shell, run:

python create_db.py db migrate -m "new"
pyrhon create_db.py db upgrade

OR

python create_db.py shell
>>>from create_db import db
>>>db.drop_all()
>>>db.create_all()
>>>quit()
$ python create_db.py db stamp heads
$ python create_db.py db migrate -m "new"
$ python create_db.py db upgrade
'''
from flask import Flask
import connexion
import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from application.app import flask_app
from application.common.foundation import db

from application.models.user_model import UserModel
from application.models.pwresources_model import PWResourcesModel
from application.models.route_model import RouteModel
from application.models.route_model import CpuIOModel,DiskIOModel,LoadAverageModel,NetworkModel,OnlineUserAmountModel
from application.models.thunderservice_model import ThunderserviceModel
from application.models.usergroup_model import UserGroupModel
from application.models.tracking_model import TrackingModel
from application.models.order_model import OrderModel
from application.models.setting_model import SettingModel



def create_app():
    app = connexion.FlaskApp(__name__, specification_dir='openapi/')
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

migrate = Migrate(flask_app,db)
manager =Manager(flask_app,db)
manager.add_command("db",MigrateCommand)


if __name__ == '__main__':
    manager.run()
