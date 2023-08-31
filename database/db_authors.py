from sqlalchemy.orm import Session, sessionmaker

from database.database import SessionLocal
from models.Model import Author, Book, City
from schemas.AuthorsSchemas import AuthorCreate


def create_author(request: AuthorCreate, db: Session):
    author = Author(name=request.name, user_id=request.user_id)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_author(id, db: Session):
    return db.query(Author).filter(Author.id == id).first()


class Abcde(City, sessionmaker):
    def __init__(self):
        super().__init__()
        self.db = SessionLocal()
        self.data = self.db.query(Book).filter(Book.id == 1).first()
        # self.data.name = "zzzz"

        # self.db.commit()
        # self.db.refresh(self.data)
        # print(db.query(Book).filter(Book.id == 1).first().name)
        # print(Depends(get_db).query(Book).filter(Book.id == 1).first())

    def get_borrowing(self, id):
        db_user = self.db.query(City).filter(City.id == 1).first()
        # self.data = db_user
        # self.name = db_user.name
        return db_user

    def commit(self):
        try:
            self.data.name = self.name
            self.db.commit()
        except AttributeError:
            self.db.commit()

    def refresh(self, ref=None):
        self.db.refresh(self.data)

    def add(self):
        self.db.add(City)


class optes(Abcde):
    def __init__(self):
        super().__init__()

    def update(self, name, author_id=None):
        self.name = name
        self.author_id = author_id
