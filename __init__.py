from flask import Flask
# ADMIN
from routes.admin.account import account_route
from routes.admin.module import module_route
from routes.admin.role import role_route
from routes.admin.permission import permission_route
from routes.admin.device import device_route

# from routes.admin.account import account_route
# from routes.admin.module import module_route
# from routes.admin.role import role_route
# from routes.admin.permission import permission_route
from routes.admin.moduleAuthorization import module_role_route
import threading
from controllers.patient.dashboard import generate_heartbeat, generate_temperature
from routes.admin.dashboard import admin_dashboard_route

# DOCTOR
# from routes.doctor.patient import patient_route

# PATIENT
from routes.patient.diagnosis import diagnosis_route
from routes.patient.dashboard import dashboard_route
from routes.category.Medicine.medicine import medicine_route
from controllers.patient.Diagnosis.Prediction.scheduledPredict import ScheduledDiagnosis
from routes.patient.patientRecord.patientRecord import patient_record_route
from routes.patient.healthInsurance.healthInsurance import health_insurance_route
#CATEGORY
from routes.category.Prescription.prescription import prescription_route
from routes.category.Doctor.doctor import doctor_route

from routes.patient.profile import patient_profile_route

def create_app():
    app = Flask(__name__)

    url_prefix = '/api'
    ############################################################
    ######################ADMIN BLUEPRINT#######################
    app.register_blueprint(account_route, url_prefix = url_prefix)
    app.register_blueprint(module_route, url_prefix = url_prefix)
    app.register_blueprint(role_route, url_prefix = url_prefix)
    app.register_blueprint(device_route, url_prefix = url_prefix)
    # app.register_blueprint(patient_route, url_prefix = url_prefix)
    # app.register_blueprint(account_route, url_prefix = url_prefix)
    # app.register_blueprint(module_route, url_prefix = url_prefix)
    # app.register_blueprint(role_route, url_prefix = url_prefix)
    # app.register_blueprint(permission_route, url_prefix = url_prefix)
    app.register_blueprint(module_role_route, url_prefix=url_prefix)
    app.register_blueprint(admin_dashboard_route, url_prefix=url_prefix)
    
    ############################################################
    ############################################################


    ############################################################
    ######################PATIENT BLUEPRINT#####################
    app.register_blueprint(diagnosis_route, url_prefix = url_prefix)
    app.register_blueprint(patient_profile_route, url_prefix=url_prefix)
    diagnosis_service = ScheduledDiagnosis()
    threading.Thread(target=diagnosis_service.run_scheduler, daemon=True).start()

    threading.Thread(target=generate_heartbeat, daemon=True).start()
    threading.Thread(target=generate_temperature, daemon=True).start()
    app.register_blueprint(dashboard_route, url_prefix= url_prefix)
    ############################################################
    ############################################################


    ############################################################
    ######################DOCTOR BLUEPRINT######################
    app.register_blueprint(permission_route, url_prefix = url_prefix)
    app.register_blueprint(prescription_route, url_prefix = url_prefix)
    app.register_blueprint(medicine_route, url_prefix = url_prefix)
    app.register_blueprint(doctor_route, url_prefix = url_prefix)
    app.register_blueprint(patient_record_route, url_prefix = url_prefix)
    app.register_blueprint(health_insurance_route, url_prefix=url_prefix)
    
    ############################################################
    ############################################################
    return app
