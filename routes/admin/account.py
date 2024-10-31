from flask import Blueprint
from controllers.admin.account import register, login, get_all, get_account_on_role
account_route = Blueprint('account',__name__)

@account_route.route('/register', methods = ['POST'])
def register_account():
    return register()

@account_route.route('/login', methods = ['POST'])
def login_account():
    return login()

@account_route.route('/accounts', methods = ['GET'])
def get_all_account():
    return get_all()

@account_route.route('/account-role/accountId=<int:account_id>', methods = ['GET'])
def get_role_by_account(account_id):
    return get_account_on_role(account_id)