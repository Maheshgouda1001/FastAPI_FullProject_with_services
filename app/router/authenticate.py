from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.authenticate import register_user, login_user
from app.db.database import SessionLocal
from app.schema.authenticate import UserRegister, LoginOut, RegisterOut, UserLogin, TokenRefreshRequest, TokenResponse
from app.utils.jwt import verify_refresh_token, create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=RegisterOut)
def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        return register_user(user, db)
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=e.args[0])

@router.post("/login", response_model=LoginOut)
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        return login_user(user, db)
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=e.args[0])

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: TokenRefreshRequest):
    try:
        payload = verify_refresh_token(request.refresh_token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        new_access_token = create_access_token({
            "name": payload.get("name"),
            "cwid": payload.get("cwid")
        })
        return {"access_token": new_access_token}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
