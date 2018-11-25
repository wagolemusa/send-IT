import os

from __init__ import create_app
from flask_jwt_extended import JWTManager


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)