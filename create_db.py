
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from application.app import flask_app

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = flask_app.config['SQLALCHEMY_DATABASE_URI']
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"]=True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)

migrate = Migrate(app,db)
manager =Manager(app,db)
manager.add_command("db",MigrateCommand)

class Role(db.Model): #需继承模型
    __tablename__="roles" #db中表明，如果不设置，则会与class同的默认名
    id=db.Column(db.Integer,primary_key=True) #SQLAlchemy要求必须有主键，一般命名为id即可
    name=db.Column(db.String(50),unique=True) #表示name为字符串，不重复

from application.models.user_model import UserModel
from application.models.pwresources_model import PWResourcesModel
from application.models.route_model import RouteModel
from application.models.thunderservice_model import ThunderserviceModel
from application.models.usergroup_model import UserGroupModel

if __name__ == '__main__':
    manager.run()