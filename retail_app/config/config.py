import os

class Config:

    DB_USERNAME = "postgres"
    DB_PASSWORD = "Gopika%4097"
    DB_HOST = "localhost"
    DB_PORT = "3306"
    DB_NAME = "postgres"

    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    SECRET_KEY = "211d73fe054939ff242fcf535e05d075c8a93b97aeae6081"
    JWT_SECRET_KEY = "d570f75df2a2a47e4e920589360fb10998bd19cdd863e7e1"
    JWT_ACCESS_TOKEN_EXPIRES = 900  
    JWT_REFRESH_TOKEN_EXPIRES = 86400  
    MAIL_SERVER = 'smtp.gmail.com'          
    MAIL_PORT = 587                         
    MAIL_USE_TLS = True                     
    MAIL_USE_SSL = False                    
    MAIL_USERNAME = 'gopika.na@techversantinfotech.com'  
    MAIL_PASSWORD = 'dfsk bqce dibw emag'     
    MAIL_DEFAULT_SENDER = ('Gopika', 'gopika.na@techversantinfotech.com')


    ENCRYPT_KEY = "4f39fced64abffb9beea2101cf7e125de6fa2725fe002e6b050509ddaea458d0"
    ENCRYPT_NONCE = "35d49b27e079b09a371c9093"


   
