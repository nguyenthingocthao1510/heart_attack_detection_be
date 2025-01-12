from flask import Blueprint, jsonify
from controllers.patient.dashboard import get_avg_BPM,get_heartbeat

dashboard_route = Blueprint('dashboard', __name__)

@dashboard_route.route('/heartbeat', methods=['GET'])
def get_heart_beat_info():
    return get_heartbeat()

@dashboard_route.route('/avg-BPM', methods=['GET'])
def get_avg_bpm():
    return get_avg_BPM()

