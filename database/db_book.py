from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Session

from database.database import engine
from models.Model import Book
from schemas.BaseResponse import BaseResponse
from schemas.BooksSchemas import BookCreate


def create_book_old(request: BookCreate, db: Session):
    books = Book(
        title=request.title,
        author_id=request.author_id
    )
    db.add(books)
    db.commit()
    db.refresh(books)
    return books


def create_book(request) -> BaseResponse:
    new_book = {
        "title": 'Example Book',
        "publication_date": datetime(2020, 1, 1),
        "isbn": '1234567890',
        "price": 10,
        "author_id": 1,
        "is_active": True,
        "soft_delete": False,
        "created_at": datetime(2020, 1, 1),
        "updated_at": datetime(2020, 1, 1),
    }

    with Session(bind=engine) as session:
        try:
            new_book = Book(
                title=request.title,
                publication_date=request.publication_date,
                isbn=request.isbn,
                price=request.price,
                author_id=request.author_id,
                is_active=request.is_active,
                soft_delete=request.soft_delete
            )
            session.add(new_book)
            session.commit()
            print("Insertion successful!")
        except Exception as e:
            print("Error occurred during insertion:", str(e))

        data = [
            {
                'title': new_book["title"],
                'publication_date': new_book["publication_date"],
                'isbn': new_book["isbn"],
                'price': new_book["price"],
                'author_id': new_book["author_id"],
                'is_active': new_book["is_active"],
                'soft_delete': new_book["soft_delete"],
                'created_at': new_book["created_at"],
                'updated_at': new_book["updated_at"]
            }
        ]

    response = BaseResponse(
        message={'field': '', 'message': 'get all cities successfully'},
        data=data
    )
    return response


def get_book(id, db: Session):
    return db.query(Book).filter(Book.id == id).first()
