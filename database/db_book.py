from sqlalchemy.orm import Session

from models.Model import Author, User, Book
from schemas.BooksSchemas import BookCreate
from utility.hash import Hash


def create_book(request: BookCreate, db: Session):
    books = Book(
            title=request.title,
            author_id=request.author_id
        )
    db.add(books)
    db.commit()
    db.refresh(books)
    return books


def get_book(id, db: Session):
    return db.query(Book).filter(Book.id == id).first()

