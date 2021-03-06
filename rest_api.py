import logging
import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from DronesAPI.database.db import db
from DronesAPI.resources.camera import Camera, Cameras, CamerasByModel, CameraRegister
from DronesAPI.resources.drone import DroneBySerial, DroneByName, Drones, DroneRegister, DronesByName,\
                                      DronesBySerialnumber
from DronesAPI.resources.user import User, UsersByName, UserLogin, Users, UserRegister, UserAdminRegister
from DronesAPI.tools.logger import set_logger
from DronesAPI.settings import DATABASE_LOC
from DronesAPI.creds import APP_SECRET_KEY


set_logger()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", DATABASE_LOC)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = APP_SECRET_KEY
api = Api(app)
db.init_app(app)

jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {
            "description": "Token has expired!",
            "error": "token_expired"
        }, 401
    )


@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify(
        {
            "description": "Signature verification failed!",
            "error": "invalid_token"
        }, 401
    )


@jwt.unauthorized_loader
def unauthorized_loader_callback(error):
    return jsonify(
        {
            "description": "Access token not found!",
            "error": "unauthorized_loader"
        }, 401
    )


@jwt.needs_fresh_token_loader
def fresh_token_loader_callback():
    return jsonify(
        {
            "description": "Token is not fresh. Fresh token needed!",
            "error": "needs_fresh_token"
        }, 401
    )


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return identity


api.add_resource(UserRegister, "/user/register")
api.add_resource(UserAdminRegister, "/user/adminregister")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(Users, "/user")
api.add_resource(UsersByName, "/user/sort/name")
api.add_resource(UserLogin, "/login")
api.add_resource(CameraRegister, "/camera/register")
api.add_resource(Camera, "/camera/<model>")
api.add_resource(Cameras, "/camera")
api.add_resource(CamerasByModel, "/camera/sort/model")
api.add_resource(DroneRegister, "/drone/register")
api.add_resource(DroneBySerial, "/drone/serial/<int:serial_number>")
api.add_resource(DroneByName, "/drone/name/<name>")
api.add_resource(Drones, "/drone")
api.add_resource(DronesBySerialnumber, "/drone/sort/serialnumber")
api.add_resource(DronesByName, "/drone/sort/name")


if __name__ == '__main__':

    @app.before_first_request
    def create_tables():
        db.create_all()

    logging.info('Execution started')
    app.run(port=5000, debug=True)
