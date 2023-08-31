from sqlalchemy import text
from sqlalchemy.orm import Session

from database.database import engine
from schemas.BaseResponse import BaseResponse


def view_book() -> BaseResponse:
    with Session(bind=engine) as session:
        result = session.execute(text("SELECT id, title,publication_date,isbn,author_id,genre_id, price,is_active, soft_delete, created_at, updated_at FROM books WHERE is_active = TRUE and soft_delete = FALSE"))
    data = [
        {
            "id": row.id,
            "title": row.title,
            "publication_date": row.publication_date,
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
