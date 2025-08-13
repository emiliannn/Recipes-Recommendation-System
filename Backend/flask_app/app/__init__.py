from flask import Flask
# from app.extensions import db
from config import Config
from flask_cors import CORS




def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, origins="http://localhost:4200")

    from app.recommendations import bp as recommendations_bp
    app.register_blueprint(recommendations_bp)  

    from app.management import bp as management_bp
    app.register_blueprint(management_bp)

  

    return app