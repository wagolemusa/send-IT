from flask import Flask
from __init__ import api_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'djrefuge'

app.register_blueprint(api_bp, url_prefix='/api')


if __name__ == "__main__":
	app.run(debug=True)