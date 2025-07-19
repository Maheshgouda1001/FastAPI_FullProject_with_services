from sqlalchemy.orm import Session
from app.schema.authenticate import UserRegister, UserLogin
from app.model.authenticate import User
from app.utils.hash import hash_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token

def register_user(user: UserRegister, db: Session):
    try:
        new_user = User(
            name=user.name,
            email=user.email,
            mobile=user.mobile,
            cwid=user.cwid,
            password=hash_password(user.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully"}
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error creating user: {e}")

def login_user(user: UserLogin, db: Session):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            raise ValueError("User not found")
        if not verify_password(user.password, db_user.password):
            raise ValueError("Incorrect password")
        return {
            "accessToken": create_access_token({"name": db_user.name, "cwid": db_user.cwid}),
            "refreshToken": create_refresh_token({"name": db_user.name, "cwid": db_user.cwid})
        }
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error logging in user: {e}")
