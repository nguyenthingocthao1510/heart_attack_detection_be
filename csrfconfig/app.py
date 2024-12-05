import os
from flask_wtf import CSRFProtect
from flask import Flask

def CSRFConfig(app):
    WTFORM_SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = WTFORM_SECRET_KEY
    csrf = CSRFProtect(app)

    return csrf