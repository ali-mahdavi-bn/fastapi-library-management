from sqlalchemy.orm import Session

from models.Model import Author
from schemas.AuthorsSchemas import AuthorCreate


def create_author(request: AuthorCreate, db: Session):
    author = Author(name=request.name, user_id=request.user_id)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_author(id, db: Session):
    return db.query(Author).filter(Author.id == id).first()
