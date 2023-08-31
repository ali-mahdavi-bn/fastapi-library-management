from sqlalchemy import text
from sqlalchemy.orm import Session

from database.database import engine
from schemas.BaseResponse import BaseResponse


def view_city() -> BaseResponse:
    with Session(bind=engine) as session:
        # a = session.query(Book).filter(Book.id == 3).first()
        # print(a.author.user.id)
        result = ""
        try:
            result = session.execute(text("select id, name, is_active, soft_delete, created_at, updated_at from cities"))
        except Exception as e:
            raise ValueError(e)
        data = [
            {
                "id": row.id,
                "title": row.name,
                "is_active": row.is_active,
                "soft_delete": row.soft_delete,
                "created_at": row.created_at,
                "updated_at": row.updated_at,
            }
            for row in result
        ]
    response = BaseResponse(
        message={'field': '', 'message': 'get all cities successfully'},
        data=data
    )
    return response
