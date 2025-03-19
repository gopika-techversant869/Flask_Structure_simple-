from flask_simple.dbService.dbCommonService import BaseRepository
from flask_simple.models.userModels import User
from flask_simple.schemas.userSchemaService import UserCreate,UserResponse

class UserService:
    """Handles business logic for Users."""

    def __init__(self):
        self.repository = BaseRepository(User)  

    def create_user(self, user_data: UserCreate):
        user = User(name=user_data.name, email=user_data.email)
        return self.repository.create(user)

    def get_users(self):
        return self.repository.get_all()

    def get_user(self, user_id):
        return self.repository.get_by_id(user_id)

    def delete_user(self, user_id):
        user = self.repository.get_by_id(user_id)
        if user:
            self.repository.delete(user)
            return True
        return False
