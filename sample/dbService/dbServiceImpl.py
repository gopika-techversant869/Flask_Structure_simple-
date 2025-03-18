# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()


from sample import db

class BaseRepository:
    """Generic repository for CRUD operations on any SQLAlchemy model."""

    def __init__(self, model):
        self.model = model  
        
    def create(self, instance):
        db.session.add(instance)
        db.session.commit()
        return instance

    def get_all(self):
        return self.model.query.all()

    def get_by_id(self, record_id):
        return self.model.query.get(record_id)

    def update(self):
        db.session.commit()

    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()
