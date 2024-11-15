from flask import Blueprint
from controllers.admin.role import get_all, get_by_id, add, update, delete

role_route = Blueprint('role', __name__)

@role_route.route('/roles', methods = ['GET'])
def get_all_role():
    return get_all()

@role_route.route('/role/id=<int:id>', methods = ['GET'])
def get_role_by_id(id):
    return get_by_id(id)

@role_route.route('/role/add', methods = ['POST'])
def add_role():
    return add()

@role_route.route('/role/update/id=<int:id>', methods = ['PUT'])
def update_role(id):
    return update(id)

@role_route.route('/role/delete/id=<int:id>', methods = ['DELETE'])
def delete_role(id):
    return delete(id)