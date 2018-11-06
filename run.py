from flask import Flask

from __init__ import v1

app = Flask(__name__)
app.config['SECRET_KEY'] = 'djrefuge'

app.register_blueprint(v1, url_prefix='/api')


if __name__ == "__main__":
	app.run(debug=True)