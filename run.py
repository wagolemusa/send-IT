import os

from __init__ import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
app.config['SECRET_KEY'] = 'refuge'


if __name__ == '__main__':
    app.run()