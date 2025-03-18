from sample.dbService.dbServiceImpl import BaseRepository
from sample.dbService.models import User
from schemas import UserCreate

class UserService:
    """Handles business logic for Users."""

    def __init__(self):
        self.repository = BaseRepository(User)  # Pass User model dynamically

    def create_user(self, user_data: UserCreate):
        """Business logic before inserting into DB"""
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
