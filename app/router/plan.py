from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.planningelements import get_user_roles, get_plans, get_all_plans
from app.db.database import SessionLocal
from app.schema.authenticate import RolesOut, JWTUserDetails, AllPlansOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/roles", response_model=RolesOut)
async def roles(request: Request, db: Session = Depends(get_db)):
    try:
        user = JWTUserDetails(**request.state.user)
        return await get_user_roles(user, db)
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=e.args[0])

@router.get("/plans")
def plans(request: Request, db: Session = Depends(get_db)):
    try:
        user = JWTUserDetails(**request.state.user)
        return get_plans(user, db)
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=e.args[0])

@router.get("/allplans", response_model=AllPlansOut)
def allplans(request: Request, db: Session = Depends(get_db)):
    try:
        user = JWTUserDetails(**request.state.user)
        return get_all_plans(user, db)
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=e.args[0])
