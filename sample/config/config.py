import os

class Config:

    DB_USERNAME = "root"
    DB_PASSWORD = "gopika-27"
    DB_HOST = "localhost"
    DB_PORT = "3306"
    DB_NAME = "test_db"

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


   
