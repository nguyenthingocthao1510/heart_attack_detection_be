from flask import Blueprint
from controllers.admin.module import get_all, get_by_id, add, update, delete

module_route = Blueprint('module', __name__)

@module_route.route('/modules', methods = ['GET'])
def get_all_module():
    return get_all()

@module_route.route('/module/id=<int:id>', methods = ['GET'])
def get_module_by_id(id):
    return get_by_id(id)

@module_route.route('/module/add', methods = ['POST'])
def add_module():
    return add()

@module_route.route('/module/update/id=<int:id>', methods = ['PUT'])
def update_module(id):
    return update(id)

@module_route.route('/module/delete/id=<int:id>', methods = ['DELETE'])
def delete_module(id):
    return delete(id)