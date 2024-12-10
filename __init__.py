from flask import Flask
# ADMIN
from routes.admin.account import account_route
from routes.admin.module import module_route
from routes.admin.role import role_route
from routes.admin.permission import permission_route

# from routes.admin.account import account_route
# from routes.admin.module import module_route
# from routes.admin.role import role_route
# from routes.admin.permission import permission_route
from routes.admin.moduleAuthorization import module_role_route
import threading
from controllers.patient.dashboard import generate_heartbeat, generate_temperature

# DOCTOR
# from routes.doctor.patient import patient_route

# PATIENT
from routes.patient.diagnosis import diagnosis_route
from routes.patient.dashboard import dashboard_route
from routes.category.Medicine.medicine import medicine_route
from controllers.patient.Diagnosis.scheduledPredict import ScheduledDiagnosis

#CATEGORY
from routes.category.Prescription.prescription import prescription_route
from routes.category.Doctor.doctor import doctor_route

from routes.patient.profile import patient_personal_info_route

def create_app():
    app = Flask(__name__)

    url_prefix = '/api'

    app.register_blueprint(account_route, url_prefix = url_prefix)
    app.register_blueprint(module_route, url_prefix = url_prefix)
    app.register_blueprint(role_route, url_prefix = url_prefix)
    # app.register_blueprint(patient_route, url_prefix = url_prefix)
    # app.register_blueprint(account_route, url_prefix = url_prefix)
    # app.register_blueprint(module_route, url_prefix = url_prefix)
    # app.register_blueprint(role_route, url_prefix = url_prefix)
    # app.register_blueprint(permission_route, url_prefix = url_prefix)
    app.register_blueprint(module_role_route, url_prefix=url_prefix)
    
    app.register_blueprint(diagnosis_route, url_prefix = url_prefix)
    app.register_blueprint(patient_personal_info_route, url_prefix=url_prefix)
    threading.Thread(target=ScheduledDiagnosis.run_scheduler, daemon=True).start()

    threading.Thread(target=generate_heartbeat, daemon=True).start()
    threading.Thread(target=generate_temperature, daemon=True).start()
    app.register_blueprint(dashboard_route, url_prefix= url_prefix)
    app.register_blueprint(permission_route, url_prefix = url_prefix)
    app.register_blueprint(prescription_route, url_prefix = url_prefix)
    app.register_blueprint(medicine_route, url_prefix = url_prefix)
    app.register_blueprint(doctor_route, url_prefix = url_prefix)
    
    return app
