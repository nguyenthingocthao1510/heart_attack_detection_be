
from flask import Flask
from routes.doctor.patient import patient_route

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(patient_route)
    
    return app
