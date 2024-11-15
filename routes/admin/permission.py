from flask import Blueprint, request, jsonify
from controllers.admin.permission import get_all_permission_in_role_module, get_all_permission_not_in_role_module, insert_permission_into_role_module, delete_permission_into_role_module, load_all_permission_information

permission_route = Blueprint('permission_module_role',__name__)

@permission_route.route('/permission-in-role-module/roleId=<int:role_id>/moduleId=<int:module_id>')
def get_all_module_permission_in_role(role_id, module_id):
    return get_all_permission_in_role_module(role_id, module_id)

@permission_route.route('/permission-not-in-role-module/roleId=<int:role_id>/moduleId=<int:module_id>')
def get_all_module_permission_not_in_role(role_id, module_id):
    return get_all_permission_not_in_role_module(role_id, module_id)

@permission_route.route('/add-permission-to-role-module', methods = ['POST'])
def add_permission_to_role_module():
    data = request.get_json()
    module_id = data['module_id']
    role_id = data['role_id']
    permission_ids = data['permission_ids']

    if role_id is not None and module_id is not None and permission_ids: 
        return insert_permission_into_role_module(module_id, role_id, permission_ids)
    else:
        return jsonify({'error': 'role_id , module_id and permission_ids are required'}), 400
    
@permission_route.route('/remove-permission-from-role-module', methods = ['DELETE'])
def delete_permission_to_role_module():
    data = request.get_json()
    module_id = data['module_id']
    role_id = data['role_id']
    permission_ids = data['permission_ids']

    result = delete_permission_into_role_module(module_id, role_id, permission_ids)
    return result

@permission_route.route('/get-all-permission/roleId=<int:role_id>')
def get_all_permission(role_id):
    return load_all_permission_information(role_id)

