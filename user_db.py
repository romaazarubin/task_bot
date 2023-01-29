from db_gino import TimedBaseModel
from sqlalchemy import Column, BigInteger, String, Integer, sql

class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    name = Column(String(200))
    random_number = Column(Integer)

    query: sql.select