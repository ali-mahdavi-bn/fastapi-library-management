from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Date
from sqlalchemy import func
from sqlalchemy.orm import relationship

from database.database import Base


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city_id = Column(Integer, ForeignKey('cities.id'))
    is_active = Column(Boolean, default=True)
    soft_delete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    city = relationship('City', back_populates='authors')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates="items", uselist=False)
    books = relationship('Book', back_populates='author')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(75), nullable=False)
    last_name = Column(String(75), nullable=False)
    username = Column(String(75), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)
    membership_type = Column(String(50))
    membership_expiry = Column(Date)
    code = Column(String(20), nullable=True)
    isUsed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    items = relationship('Author', back_populates='user')



class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    descriptions = Column(String, index=True)
    publication_date = Column(DateTime)
    isbn = Column(String, index=True)
    price = Column(Integer)
    is_active = Column(Boolean, default=True)
    soft_delete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    genre_id = Column(Integer, ForeignKey('genres.id'))  # Add a foreign key column to reference the genre table
    author_id = Column(Integer, ForeignKey('authors.id'))
    borrowing = relationship("Borrowing", backref="borrowings_books")
    genre = relationship("Genre", back_populates="books")
    author = relationship('Author', backref="author_books")


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    authors = relationship('Author', back_populates='city', uselist=False)
    is_active = Column(Boolean, default=True)
    soft_delete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Borrowing(Base):
    __tablename__ = 'borrowings'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    borrowed_at = Column(DateTime, default=datetime.now)
    expertime_at = Column(DateTime, default=datetime.now)
    taken_back_at = Column(DateTime, nullable=True)
    book = relationship('Book', backref="borrowing_books")
    user = relationship('User', backref="borrowing_users")
    is_active = Column(Boolean, default=True)
    soft_delete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    soft_delete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    books = relationship("Book", back_populates="genre")  # Add a relationship to the Book class
    # genres = relationship('Genre', back_populates='genre', overlaps="genres_books")
