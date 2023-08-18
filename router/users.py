from datetime import datetime

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.db_user import create_user
from schemas.BaseResponse import BaseResponseUser, validate_response
from schemas.UserSchemas import UserOut, UserCreate
from utility.get_db import get_db

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = create_user(request=user, db=db)

        data = UserOut(
            id=db_user.id,
            name=db_user.name,
            username=db_user.username,
            email=db_user.email,
            role=db_user.role,
        )

        response = BaseResponseUser(
            message={'field': '', 'message': 'Registration is successful'},
            data=data,
        )

        return response
    except IntegrityError:
        raise HTTPException(detail=validate_response("email", {
            "email": "Email is already exists",
        }), status_code=status.HTTP_400_BAD_REQUEST)
