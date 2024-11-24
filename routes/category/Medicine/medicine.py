from flask import Blueprint
from controllers.category.Medicine.medicine import get_all

medicine_route = Blueprint('medicine_route',__name__)

@medicine_route.route('/medicines', methods = ['GET'])
def get_all_medicine():
    return get_all()