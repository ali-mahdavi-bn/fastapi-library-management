from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.db_borrowing import create_borrowing, get_borrowing
from schemas.BaseResponse import BaseResponseBorrowing, validate_response
from schemas.BrowingSchemas import BorrowingCreate, BorrowingOut, BorrowingUpdate, BorrowingOutUpdate
from utility.get_db import get_db

router = APIRouter()


@router.post("/Borrowing/")
def create_Borrowing_api(book: BorrowingCreate, db: Session = Depends(get_db)):
    try:
        db_borrowing = create_borrowing(request=book, db=db)

        data = BorrowingOut(
            book_id=db_borrowing.book_id,
            user_id=db_borrowing.user_id,
            borrowed_at=db_borrowing.borrowed_at,
            expertime_at=db_borrowing.expertime_at,
            taken_back_at=db_borrowing.taken_back_at,
        )

        response = BaseResponseBorrowing(
            message={'field': '', 'message': 'Data storage is successful'},
            data=data,
        )

        return response
    except IntegrityError:
        raise HTTPException(detail=validate_response("", {
            "error_create": "Data storage problem",
        }), status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/borrowings/{borrowing_id}")
async def get_borrowing_api(borrowing_id: int, db: Session = Depends(get_db)):
    borrowing = get_borrowing(borrowing_id, db)
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    return borrowing


@router.put("/borrowings/{borrowing_id}")
async def update_borrowing_api(borrowing_id: int, borrowing: BorrowingUpdate, db: Session = Depends(get_db)):
    existing_borrowing = get_borrowing(borrowing_id, db)
    if not existing_borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    for field, value in borrowing.dict().items():
        setattr(existing_borrowing, field, value)
    db.commit()
    db.refresh(existing_borrowing)

    data = BorrowingOutUpdate(
        book_id=existing_borrowing.book_id,
        user_id=existing_borrowing.user_id,
        borrowed_at=existing_borrowing.borrowed_at,
        expertime_at=existing_borrowing.expertime_at,
        taken_back_at=existing_borrowing.taken_back_at,
        is_active=existing_borrowing.is_active,
        soft_delete=existing_borrowing.soft_delete,

    )
    response = BaseResponseBorrowing(
        message={'field': '', 'message': 'Data storage is successful'},
        data=data,
    )

    return response


@router.delete("/borrowings/{borrowing_id}")
async def delete_borrowing_api(borrowing_id: int, db: Session = Depends(get_db)):
    borrowing = get_borrowing(borrowing_id, db)
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    borrowing.soft_delete = True
    db.commit()
    db.refresh(borrowing)
    return {"message": "Borrowing deleted successfully"}


#
#

#
# @app.delete("/authors/{author_id}")
# async def delete_author(author_id: int, db: Session = Depends(get_db)):
#     author = db.query(Author).filter(Author.id == author_id).first()
#     if not author:
#         raise HTTPException(status_code=404, detail="Author not found")
#     db.delete(author)
#     db.commit()
#     return {"message": "Author deleted successfully"}
#
# # CRUD operations for Users
#
# @app.post("/users")
# async def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     new_user = User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
#
# @app.get("/users/{user_id}")
# async def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#
# @app.put("/users/{user_id}")
# async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.id == user_id).first()
#     if not existing_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     for field, value in user.dict().items():
#         setattr(existing_user, field, value)
#     db.commit()
#     db.refresh(existing_user)
#     return existing_user
#
# @app.delete("/users/{user_id}")
# async def delete_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(user)
#     db.commit()
#     return {"message": "User deleted successfully"}
