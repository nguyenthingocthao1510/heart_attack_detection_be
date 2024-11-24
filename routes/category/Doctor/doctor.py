from flask import Blueprint
from controllers.category.Doctor.doctor import get_all

doctor_route = Blueprint('doctor_route', __name__)
@doctor_route.route('/doctors', methods = ['GET'])
def get_all_doctor():
    return get_all()