from flask import Blueprint, jsonify
from controllers.patient.dashboard import get_latest_heartbeats, get_latest_temperature

dashboard_route = Blueprint('dashboard', __name__)

@dashboard_route.route('/heartbeat', methods=['GET'])
def get_heartbeat():
    heartbeat = get_latest_heartbeats()
    if heartbeat:
        return jsonify(heartbeat)  # Trả về heartbeat mới nhất
    else:
        return jsonify({'error': 'Waiting for heartbeat data... Please try again after a minute.'}), 503
    

@dashboard_route.route('/temperature', methods=['GET'])
def get_temperature():
    temperature = get_latest_temperature()
    if temperature:
        return jsonify(temperature) 
    else:
        return jsonify({'error': 'Waiting for heartbeat data... Please try again after a minute.'}), 503

