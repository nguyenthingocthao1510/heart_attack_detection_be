
from flask import Flask
# ADMIN
# from routes.admin.account import account_route
# from routes.admin.module import module_route
# from routes.admin.role import role_route
# from routes.admin.permission import permission_route
# from routes.admin.moduleRole import module_role_route

# DOCTOR
# from routes.doctor.patient import patient_route

# PATIENT
from routes.patient.diagnose import diagnosis_route

def create_app():
    app = Flask(__name__)
    
    url_prefix = '/api'

    # app.register_blueprint(patient_route, url_prefix = url_prefix)
    # app.register_blueprint(account_route, url_prefix = url_prefix)
    # app.register_blueprint(module_route, url_prefix = url_prefix)
    # app.register_blueprint(role_route, url_prefix = url_prefix)
    # app.register_blueprint(permission_route, url_prefix = url_prefix)
    # app.register_blueprint(module_role_route, url_prefix=url_prefix)

    app.register_blueprint(diagnosis_route, url_prefix = url_prefix)

    return app
