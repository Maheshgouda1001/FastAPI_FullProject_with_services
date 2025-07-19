from sqlalchemy import Column, Integer, String, Date
from app.db.database import Base

class PlanningElements(Base):
    __tablename__ = "planning_elements"
    id = Column(Integer, primary_key=True, index=True)
    plan = Column(String)
    opening_date = Column(Date)
    closing_date = Column(Date)
