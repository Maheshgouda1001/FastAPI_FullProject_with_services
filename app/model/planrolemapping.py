from sqlalchemy import Column, Integer, ForeignKey, Boolean
from app.db.database import Base

class PlanRoleMapping(Base):
    __tablename__ = "plan_role_mapping"
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("planning_elements.id"), index=True)
    role_id = Column(Integer, ForeignKey("user_roles.id"), index=True)
    editable = Column(Boolean)
