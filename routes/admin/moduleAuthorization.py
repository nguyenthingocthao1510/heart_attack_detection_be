from flask import Blueprint, request, jsonify
from controllers.admin.moduleAuthorization import get_module_in_role, get_module_not_in_role, add_module_into_role, delete_module_in_role


module_role_route = Blueprint('module_role_route', __name__)

@module_role_route.route('/module-in-role/roleId=<int:role_id>', methods = ['GET'])
def get_all_module_in_role(role_id):
    return get_module_in_role(role_id)

@module_role_route.route('/module-not-in-role/roleId=<int:role_id>', methods = ['GET'])
def get_all_module_not_in_role(role_id):
    return get_module_not_in_role(role_id)

@module_role_route.route('/add-module-to-role', methods = ['POST'])
def add_module_to_role():
    data = request.get_json()
    role_id = data['role_id']
    module_ids = data['module_ids']
    
    if role_id is not None and module_ids:
        return add_module_into_role(role_id, module_ids)
    else:
        return jsonify({'error': 'role_id and module_ids are required'}), 400

@module_role_route.route('/remove-module-in-role', methods = ['DELETE'])
def remove_module_in_role():
    data = request.get_json()
    role_id = data['role_id']
    module_ids = data['module_ids']
    
    result = delete_module_in_role(role_id, module_ids)
    return jsonify(result)