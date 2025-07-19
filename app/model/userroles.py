from sqlalchemy import Column, Integer
from app.db.database import Base

class UserRoles(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, index=True)
    role = Column(Integer, index=True)
