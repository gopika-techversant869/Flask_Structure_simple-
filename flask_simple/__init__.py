from flask import Flask
from flask_migrate import Migrate
from flask_simple.dbService.db import db
from flask_simple.config import config


migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)
    print("Config Loaded:", app.config["SQLALCHEMY_DATABASE_URI"]) 

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from flask_simple.routes.user_routes import bp
        app.register_blueprint(bp, url_prefix="/api")

        db.create_all()  
    return app
