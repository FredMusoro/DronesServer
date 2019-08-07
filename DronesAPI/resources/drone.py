from flask_restful import Resource, reqparse
from flask_jwt_extended import fresh_jwt_required, get_current_user

from DronesAPI.models.drone import DroneModel
from DronesAPI.models.camera import CameraModel
from DronesAPI.models.user import UserModel

_drone_parser = reqparse.RequestParser()
_drone_parser.add_argument(
    "serial_number",
    type=str,
    required=False,
    help="This field can be blank"
)
_drone_parser.add_argument(
    "name",
    type=str,
    required=False,
    help="This field can be blank"
)
_drone_parser.add_argument(
    "brand",
    type=str,
    required=False,
    help="This field can be blank"
)
_drone_parser.add_argument(
    "cameras",
    type=str,
    required=False,
    help="This field can be blank"
)


class DroneBySerial(Resource):
    @staticmethod
    def get(serial_number):
        drone = DroneModel.find_drone_by_serial(serial_number)
        if drone:
            return process_cameras(drone)
        return {
                   "message": "Drone not found!"
               }, 404

    @fresh_jwt_required
    def delete(self, serial_number):
        user_team = UserModel.find_user_by_id(get_current_user()).team
        if user_team == 'Support':
            drone = DroneModel.find_drone_by_serial(serial_number)
            if drone:
                drone.remove_from_db()
                return {
                           "message": "Drone deleted!"
                       }

            return {
                       "message": "Drone not found!"
                   }, 404
        else:
            return {
                       "message": "Non authorized user!"
                   }, 400


class DroneByName(Resource):
    @staticmethod
    def get(name):
        drones = DroneModel.find_drones_by_name(name)
        if drones:
            output = []
            for drone in drones:
                output.append(process_cameras(drone))
            return output
        return {
                   "message": "Drone not found!"
               }, 404


class Drones(Resource):
    @staticmethod
    def get():
        drones = DroneModel.find_all_drones()
        if drones:
            output = []
            for drone in drones:
                output.append(process_cameras(drone))
            return output
        return {
                   "message": "No drones found!"
               }, 404


class DronesByName(Resource):
    @staticmethod
    def get():
        drones = DroneModel.sort_drones_by_name()
        if drones:
            output = []
            for drone in drones:
                output.append(process_cameras(drone))
            return output
        return {
                   "message": "No drones found!"
               }, 404


class DronesBySerialnumber(Resource):
    @staticmethod
    def get():
        drones = DroneModel.sort_drones_by_serialnumber()
        if drones:
            output = []
            for drone in drones:
                output.append(process_cameras(drone))
            return output
        return {
                   "message": "No drones found!"
               }, 404


class DroneRegister(Resource):

    @fresh_jwt_required
    def post(self):
        user_team = UserModel.find_user_by_id(get_current_user()).team
        if user_team == 'Support':
            data = _drone_parser.parse_args()
            for camera in data['cameras'].split(','):
                found_camera = CameraModel.find_camera_by_model(camera.strip())
                if not found_camera:
                    return {
                           "message": "Camera not correct: {}".format(camera.strip())
                       }, 400

            if DroneModel.find_drone_by_serial(data["serial_number"]):
                return {
                           "message": "Drone {} already exists".format(data["serial_number"])
                       }, 400

            drone = DroneModel(data["serial_number"], data["name"], data["brand"], data['cameras'])
            drone.save_to_db()
            return {
                "message": "Drone {} created".format(data["serial_number"])
            }
        else:
            return {
                       "message": "Non authorized user!"
                   }, 400


def process_cameras(drone):
    drone = drone.json()
    cameras = []
    for camera in drone['cameras'].split(','):
        camera = camera.strip()
        found_camera = CameraModel.find_camera_by_model(camera)
        if found_camera:
            cameras.append(found_camera.json())
    drone['cameras'] = cameras
    return drone