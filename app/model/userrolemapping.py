from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base

class UserRoleMapping(Base):
    __tablename__ = "user_role_mapping"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False, index=True)