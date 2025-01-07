from flask import Blueprint
from controllers.admin.Device.device import DeviceRepo

device_route = Blueprint('device', __name__)
deviceRepo = DeviceRepo()

@device_route.route('/get-device', methods = ['GET'])
def get_all_device():
    return deviceRepo.get_device()

@device_route.route('/unassigned-patients', methods = ['GET'])
def get_all_unassigned_patient():
    return deviceRepo.get_unassigned_patients()
