from user_db import User

async def add_user(user_id: int, name: str, random_number: int):
    try:
        user = User()