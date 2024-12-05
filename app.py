from flask import Flask
from __init__ import create_app
from flask_cors import CORS
from csrfconfig.app import CSRFConfig

app = Flask(__name__)

app = create_app()

csrf = CSRFConfig(app)

CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
