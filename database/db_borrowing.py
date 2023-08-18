from sqlalchemy.orm import Session

from models.Model import Borrowing
from schemas.AuthorsSchemas import AuthorCreate
from schemas.BrowingSchemas import BorrowingCreate


def create_borrowing(request: BorrowingCreate, db: Session):
    borrowing = Borrowing(book_id=request.book_id, user_id=request.user_id, borrowed_at=request.borrowed_at,
                          expertime_at=request.expertime_at)
    db.add(borrowing)
    db.commit()
    db.refresh(borrowing)
    return borrowing


def get_borrowing(id, db: Session):
    return db.query(Borrowing).filter(Borrowing.id == id).first()
