from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import db_authors
from database.db_authors import create_author
from schemas.AuthorsSchemas import AuthorCreate, AuthorOut, AuthorUpdate
from schemas.BaseResponse import BaseResponseAuthor, validate_response
from utility.get_db import get_db

# from utility.respone import Response

router = APIRouter()


# Create an author
# @router.post('/authors', response_model=UserOut)
# def create_author(author: AuthorCreate, db=Depends(get_db)):
#     return db_authors.create_author(author, db)


@router.post("/authors/")
def create_author_api(author: AuthorCreate, db: Session = Depends(get_db)):
    try:
        db_author = create_author(author, db)

        data = AuthorOut(
            id=db_author.id,
            name=db_author.name,
            user_id=db_author.user_id,
        )

        response = BaseResponseAuthor(
            message={'field': '', 'message': 'Data storage is successful'},
            data=data,
        )

        return response
    except IntegrityError:
        raise HTTPException(detail=validate_response("email", {
            "email": "Email is already exists",
        }), status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/authors/{author_id}")
async def get_author_api(author_id: int, db: Session = Depends(get_db)):
    author = db_authors.get_author(author_id, db)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.put("/authors/{author_id}")
async def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    existing_author = db_authors.get_author(author_id, db)
    if not existing_author:
        raise HTTPException(status_code=404, detail="Author not found")
    for field, value in author.dict().items():
        setattr(existing_author, field, value)
    db.commit()
    db.refresh(existing_author)
    return existing_author

@router.delete("/author/{author_id}")
async def delete_borrowing_api(author_id: int, db: Session = Depends(get_db)):
    author = db_authors.get_author(author_id, db)
    if not author:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    author.soft_delete = True
    db.commit()
    db.refresh(author)
    return {"message": "Borrowing deleted successfully"}
