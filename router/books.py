

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status


from database.db_book import get_book, create_book
from schemas.BaseResponse import BaseResponseBook, validate_response
from schemas.BooksSchemas import BookOut, BookCreate, BookUpdate
from utility.get_db import get_db

router = APIRouter()


#
#
@router.post("/book/")
def create_book_api(book: BookCreate, db: Session = Depends(get_db)):
    try:
        db_user = create_book(request=book, db=db)

        data = BookOut(
            title=db_user.title,
            book_id=db_user.book_id
        )

        response = BaseResponseBook(
            message={'field': '', 'message': 'Data storage is successful'},
            data=data,
        )

        return response
    except IntegrityError:
        raise HTTPException(detail=validate_response("", {
            "error_create": "Data storage problem",
        }), status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/book/{book_id}")
async def get_book_api(book_id: int, db: Session = Depends(get_db)):
    book = get_book(book_id, db)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/book/{book_id}")
async def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    existing_book = get_book(book_id, db)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for field, value in book.dict().items():
        setattr(existing_book, field, value)
    db.commit()
    db.refresh(existing_book)
    return existing_book

@router.delete("/Book/{book_id}")
async def delete_borrowing_api(book_id: int, db: Session = Depends(get_db)):
    book = get_book(book_id, db)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.soft_delete = True
    db.commit()
    db.refresh(book)
    return {"message": "Borrowing deleted successfully"}
