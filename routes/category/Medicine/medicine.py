from flask import Blueprint
from controllers.category.Medicine.medicine import get_all, get_by_id, add, update, delete

medicine_route = Blueprint('medicine_route',__name__)

@medicine_route.route('/medicines', methods = ['GET'])
def get_all_medicine():
    return get_all()

@medicine_route.route('/medicine/id=<int:id>', methods = ['GET'])
def get_medicine_by_id(id):
    return get_by_id(id)

@medicine_route.route('/medicine/create-information', methods = ['POST'])
def add_medicine():
    return add()

@medicine_route.route('/medicine/update-information/id=<int:id>', methods = ['PUT'])
def update_medicine_by_id(id):
    return update(id)

@medicine_route.route('/medicine/delete-information/id=<int:id>', methods = ['DELETE'])
def delete_medicine_by_id(id):
    return delete(id)