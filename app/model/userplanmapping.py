from sqlalchemy import Column, Integer, ForeignKey, Boolean
from app.db.database import Base

class UserPlanMapping(Base):
    __tablename__ = "user_plan_mapping"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    plan_id = Column(Integer, ForeignKey("planning_elements.id"), index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    editable = Column(Boolean)
