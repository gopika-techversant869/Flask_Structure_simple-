from flask import Flask
from flask_migrate import Migrate
from retail_app.db_service.db import db
from retail_app.db_service.db import mongo
from retail_app.config import config
from retail_app.extensions import mail


migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)
    print("Config Loaded:", app.config["SQLALCHEMY_DATABASE_URI"]) 
    print("Config Loaded:", app.config["MONGO_URI"])

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    mongo.init_app(app)
    # migrate.init_app(app,mongo)

    with app.app_context():
        from retail_app.routes.user_routes import bp
        from retail_app.routes.auth_route import auth_bp
        app.register_blueprint(bp, url_prefix="/api")
        app.register_blueprint(auth_bp, url_prefix="/auth/api")
    return app
