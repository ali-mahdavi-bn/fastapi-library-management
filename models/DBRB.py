import copy
from datetime import datetime
from typing import Union

from sqlalchemy.orm import sessionmaker

from database.database import engine
from models.Model import Book, Author
from schemas.BaseResponse import BaseResponse
from utility.CustomValidations import customvalidations

Session = sessionmaker()
Session.configure(bind=engine)


#
class EntityBook(Book):
    def __init__(self):
        self.session = Session()

    # gets
    def __get_book_saved(self, title=None, isbn=None, price=None, author_id=None, is_active=None) -> BaseResponse:
        try:
            result = self.session.query(Book).filter(Book.title == title, Book.isbn == isbn, Book.price == price,
                                                     Book.author_id == author_id).first()
        except Exception as e:
            raise ValueError(e)
        data = [
            {
                "id": result.id,
                "title": result.title,
                "descriptions": result.descriptions,
                "publication_date": result.publication_date,
                "isbn": result.isbn,
                "price": result.price,
                "genre_id": result.genre_id,
                "author_id": result.author_id,
                "is_active": result.is_active,
                "soft_delete": result.soft_delete,
                "created_at": result.created_at,
                "updated_at": result.updated_at,
            }
        ]
        return {"data": data, "result": result}

    def get_book(self, id):
        db_user = ""
        try:
            db_data = self.session.query(Book).filter(Book.id == id).first()

            self.data = db_data
            self.title = db_data.title
            self.publication_date = db_data.publication_date
            self.isbn = db_data.isbn
            self.price = db_data.price
            self.genres = db_data.genres
            self.author_id = db_data.author_id
            self.is_active = db_data.is_active
            self.soft_delete = db_data.soft_delete
            self.created_at = db_data.created_at
            self.updated_at = db_data.updated_at
        except AttributeError:
            raise ValueError("Book NotFound: %s" % id)

        return db_data

    def get_book_by_id(self, id):
        try:
            result = self.session.query(Book).filter(Book.id == id).first()
        except Exception as e:
            raise ValueError(e)
        if not result:
            raise ValueError("book id not found")
        data = [
            {
                "id": result.id,
                "title": result.title,
                "publication_date": result.publication_date,
                "price": result.price,
                "is_active": result.is_active,
                "soft_delete": result.soft_delete,
                "created_at": result.created_at,
                "updated_at": result.updated_at,
            }
        ]
        response = BaseResponse(
            message={'field': '', 'message': 'get all cities successfully'},
            data=data
        )
        return response

    def get_author(self, id: Union[int, str]) -> Union[int, str]:
        author = self.session.query(Author).filter(Author.id == id).first()
        if not author:
            raise ValueError("author not found")
        return id

    # validations
    def validate_unique_data(self, title=None, isbn=None, price=None, author_id=None):
        db_data = self.session.query(Book).filter(Book.title == title, Book.isbn == isbn, Book.price == price,
                                                  Book.author_id == author_id).first()
        if db_data:
            raise ValueError("already exist")

    def valid_unice_author(self, author_id: Union[int, str]) -> Union[int, str]:
        author = self.session.query(Book).filter(Book.author_id == author_id).first()
        if author:
            raise ValueError("author already exists")
        return author_id

    def valid_isbn(self, isbn: str) -> str:
        isbn_db = self.session.query(Book).filter(Book.isbn == isbn).first()
        if isbn_db:
            raise ValueError("isbn already exists")
        return isbn

    # entities
    def validate_string(self, value, min_length=3, max_length=75):
        if not isinstance(value, str):
            return False

        length = len(value)
        if length < min_length or length > max_length:
            return False

        return True

    def valid_unice_title(self, title):
        title_db = self.session.query(Book).filter(Book.title == title).first()
        try:

            t = title_db.title
            print(50 * "===")
            print(t)
            print(50 * "===")
            return False
        except:
            return True

    def entity_title(self, value: str) -> None:
        if self.validate_string(value):
            print(value)
            if self.valid_unice_title(value):
                self.title = value
            else:
                raise ValueError("title already exist")

        else:
            raise ValueError("Invalid entity title")

    def entity_descriptions(self, value: str) -> None:
        if customvalidations.validate_descriptions(value):
            if self.valid_unice_title(value):
                self.descriptions = value
        else:
            raise ValueError("Invalid entity descriptions")

    def entity_author(self, value):
        if customvalidations.validate_int(value):
            try:
                author = self.get_author(value)
                self.author_id = value

            except ValueError as e:
                raise ValueError(e)

    def entity_genres(self, value):
        if customvalidations.validate_int(value):
            try:
                self.genre_id = value
            except ValueError as e:
                raise ValueError(e)

    def entity_publication_date(self, value):
        if customvalidations.validate_datetime(value, "%Y-%m-%d %H:%M:%S.%f%z"):
            self.publication_date = value
        else:
            raise ValueError("Invalid entity publication_date")

    def entity_created_at(self, value):
        if customvalidations.validate_datetime(value, "%Y-%m-%d %H:%M:%S.%f%z"):
            self.created_at = value
        else:
            raise ValueError("Invalid entity created_at")

    def entity_updated_at(self, value):
        if customvalidations.validate_datetime(value, "%Y-%m-%d %H:%M:%S.%f%z"):
            self.updated_at = value
        else:
            raise ValueError("Invalid entity updated_at")

    def entity_price(self, value):
        if customvalidations.validate_int(value):
            self.price = value
        else:
            raise ValueError("Invalid entity price")

    def entity_isbn(self, value):
        if customvalidations.validate_string(value):
            try:
                author = self.valid_isbn(value)
                self.isbn = value
            except ValueError as e:
                raise ValueError(e)

    def entity_is_active(self, value):
        if customvalidations.validate_bool(value):
            self.is_active = value
        else:
            raise ValueError("Invalid entity is_active")

    def entity_soft_delete(self, value):
        if customvalidations.validate_bool(value):
            self.soft_delete = value
        else:
            raise ValueError("Invalid entity soft_delete")

    def add(self):
        self.session.add(self)

    def commit(self):
        try:
            if self.data:
                self.data.title = self.title
                self.data.descriptions = self.descriptions
                self.data.publication_date = self.publication_date
                self.data.isbn = self.isbn
                self.data.price = self.price
                self.data.genre_id = self.genre_id
                self.data.author_id = self.author_id
                self.data.is_active = self.is_active
                self.data.soft_delete = self.soft_delete
                self.data.created_at = self.created_at
                self.data.updated_at = self.updated_at

                result = copy.deepcopy(self.data)

                data = [
                    {
                        "id": result.id,
                        "title": result.title,
                        "descriptions": result.descriptions,
                        "publication_date": result.publication_date,
                        "isbn": result.isbn,
                        "price": result.price,
                        "genre_id": result.genre_id,
                        "author_id": result.author_id,
                        "is_active": result.is_active,
                        "soft_delete": result.soft_delete,
                        "created_at": result.created_at,
                        "updated_at": result.updated_at,
                    }
                ]
                response = BaseResponse(
                    message={'field': '', 'message': 'updated successfully'},
                    data=data
                )
                self.session.commit()
                return response
                self.data = None

        except AttributeError:
            self.session.commit()
            return self.__get_book_saved(title=self.title, isbn=self.isbn, price=self.price, author_id=self.author_id)

    def refresh(self, ref=None):
        self.session.refresh(self)


class BookReposetory(EntityBook):
    def create(self, title: str = None, descriptions: str = None, author_id: int = None, genre_id: int = None,
               publication_date=None,
               isbn: str = None,
               price: int = None, is_active: bool = True, soft_delete: bool = False, created_at=datetime.now(),
               updated_at=datetime.now()) -> None:
        self.entity_title(title)
        self.entity_descriptions(descriptions)
        self.entity_publication_date(publication_date)
        self.entity_author(author_id)
        self.entity_isbn(isbn)
        self.entity_price(price)
        self.entity_genres(genre_id)
        self.entity_is_active(is_active)
        self.entity_soft_delete(soft_delete)
        self.entity_created_at(created_at)
        self.entity_updated_at(updated_at)

    def reade(self, id):
        return self.get_book_by_id(id)

    def update(self, title: str = None, author_id: int = None, genre_id: int = None, publication_date=None,
               isbn: str = None,
               price: int = None, is_active: bool = True, soft_delete: bool = False, created_at=datetime.now(),
               updated_at=datetime.now()):
        self.entity_title(title)
        self.entity_publication_date(publication_date)
        self.entity_author(author_id)
        self.entity_isbn(isbn)
        self.entity_price(price)
        self.entity_genres(genre_id)
        self.entity_is_active(is_active)
        self.entity_soft_delete(soft_delete)
        self.entity_created_at(created_at)
        self.entity_updated_at(updated_at)

    def delete(self, book):
        self.session.delete(book)

    def list(self):
        # return view_book()
        result = self.session.query(Book).all()
        data = [
            {
                "id": row.id,
                "name": row.title,
                "city_id": row.publication_date,
                "isbn": row.isbn,
                "price": row.price,
                "author_id": row.author_id,
                "genre_id": row.genre_id,
                "is_active": row.is_active,
                "soft_delete": row.soft_delete,
                "created_at": row.created_at,
                "updated_at": row.updated_at,
            }
            for row in result
        ]
        response = BaseResponse(
            message={'field': '', 'message': 'get all book successfully'},
            data=data
        )
        return response
        # Book.genres = a
        # for i in a.books:
        #     print(i.genres)
        # self.session.commit()
        # print(a)

    # def update(self, title, author_id=None) -> None:
    #     self.title = title
    #     self.author_id = author_id
