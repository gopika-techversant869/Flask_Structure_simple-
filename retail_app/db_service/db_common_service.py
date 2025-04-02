from retail_app.db_service.db import db, mongo
from sqlalchemy.exc import SQLAlchemyError
from pymongo.errors import PyMongoError



class DBService:
    """Common Database Service for PostgreSQL & MongoDB"""

    
    @staticmethod
    def create_record(table, data, is_mongo=False):
        try:
            if is_mongo:
                if not isinstance(data, dict):
                  raise ValueError("  ERROR: Data must be a dictionary!")
                
                print(f"db.{table}.insertOne({data})")
                collection_name = table.__name__.lower()


                print("data",type(data.get('name')))
                print("table",table)
                result = mongo.db[collection_name].insert_one(data)
                # return result
                data["_id"] = str(result.inserted_id)  # Convert ObjectId to string

                return data
            else:
                print("table",table)
                obj = table(**data)
                db.session.add(obj)
                db.session.commit()
                return obj  
        except (SQLAlchemyError, PyMongoError) as e:
            db.session.rollback()
            return {"error": str(e)}

    @staticmethod
    def find_one(table, filters, is_mongo=False):
        if is_mongo:
            return mongo.db[table].find_one(filters)
        else:
            return table.query.filter_by(**filters).first()

    @staticmethod
    def find_all(table, filters={}, is_mongo=False):
        if is_mongo:
            return list(mongo.db[table].find(filters))
        else:
            return table.query.filter_by(**filters).all()

    @staticmethod
    def update_record(table, filters, update_data, is_mongo=False):
        if is_mongo:
            return mongo.db[table].update_one(filters, {"$set": update_data})
        else:
            record = table.query.filter_by(**filters).first()
            if record:
                for key, value in update_data.items():
                    setattr(record, key, value)
                db.session.commit()
                return True
            return False

    @staticmethod
    def delete_record(table, filters, is_mongo=False):
        if is_mongo:
            return mongo.db[table].delete_one(filters)
        else:
            record = table.query.filter_by(**filters).first()
            if record:
                db.session.delete(record)
                db.session.commit()
                return True
            return False
