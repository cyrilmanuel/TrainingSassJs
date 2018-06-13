import os

from flask import Flask, render_template
from flask_assets import Environment,Bundle

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        static_folder="../static/dist",
        template_folder="../static",
    )
    assets = Environment(app)
    assets.url = app.static_url_path
    scss = Bundle('../static/scss/materialize.scss', filters='pyscss', output='all.css')
    assets.register('scss_all', scss)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        return render_template("main.html")

    return app
