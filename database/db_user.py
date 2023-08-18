from sqlalchemy.orm import Session

from models.Model import Author, User
from schemas.UserSchemas import UserCreate
from utility.hash import Hash


def create_user(request: UserCreate, db: Session):
    user = User(
            name=request.name,
            username=request.username,
            email=request.email,
            password=Hash.hash_password(request.password),
            role=request.role,
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(id, db: Session):
    return db.query(User).filter(User.id == id).first()

