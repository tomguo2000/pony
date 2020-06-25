#!/usr/bin/env python3

import logging
import connexion
import os
from application.common.foundation import db


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


if __name__ == "__main__":
    logging.basicConfig(filename="test.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%m-%Y %H:%M:%S")
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=8080,debug=True)
