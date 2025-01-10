from flask import Blueprint
from controllers.admin.dashboard import get_activate_status, get_deactivate_status, get_assign_status, get_not_assign_status, get_medicine_information

admin_dashboard_route = Blueprint('admin_dashboard_route', __name__)
@admin_dashboard_route.route('/dashboard/account-activate', methods=['GET'])
def get_all_activate_account():
    return get_activate_status()

@admin_dashboard_route.route('/dashboard/account-deactivate', methods=['GET'])
def get_all_deactivate_account():
    return get_deactivate_status()

@admin_dashboard_route.route('/dashboard/device-assign', methods=['GET'])
def get_all_device_assign():
    return get_assign_status()

@admin_dashboard_route.route('/dashboard/device-not-assign', methods=['GET'])
def get_all_device_not_assign():
    return get_not_assign_status()

@admin_dashboard_route.route('/dashboard/medicine-information', methods=['GET'])
def get_all_medicine_information():
    return get_medicine_information()