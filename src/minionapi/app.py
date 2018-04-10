import os,logging
from flask import Flask, request
from flask import g, current_app
from minionapi.security.auth import JWTAuth
from minionapi.apis import blueprint as api


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(config or {})
    app.config.from_object(os.environ['FLASK_CONFIG'])
    app.config.from_envvar('CONFIG', silent=True)
    app.config['SECRET_KEY'] = 'super-secret'
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.register_blueprint(api)
    configure_logging(app)
    register_teardowns(app)

    # initialize JWT
    jwt_auth = JWTAuth(app)
    jwt = jwt_auth.jwt()

    return app


def configure_logging(app):
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    sh = logging.StreamHandler()
    sh.setLevel(logging.ERROR)
    sh.setFormatter(formatter)
    app.logger.addHandler(sh)
    if 'LOGGING_LOCATION' in app.config:
        fh = logging.FileHandler(app.config['LOGGING_LOCATION'])
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        app.logger.addHandler(fh)


def register_teardowns(flask_app):
    pass
    # db.close_db_factory(flask_app)


if __name__ == '__main__':
    app = create_app()

    # run flask app
    app.run(debug=True)




