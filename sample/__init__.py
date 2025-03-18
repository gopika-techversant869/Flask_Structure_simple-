from flask import Flask
from flask_migrate import Migrate
from dbService.db import db

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)  
    migrate.init_app(app, db)

    with app.app_context():
        import views  

    return app
