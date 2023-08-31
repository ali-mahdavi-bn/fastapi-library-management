from sqlalchemy import text
from sqlalchemy.orm import Session

from database.database import engine
from schemas.BaseResponse import BaseResponse


def view_author() -> BaseResponse:
    with Session(bind=engine) as session:
        result = session.execute(text("SELECT id, name,city_id,user_id, is_active, soft_delete, created_at, updated_at FROM authors WHERE is_active = TRUE and soft_delete = FALSE"))
    data = [
        {
            "id": row.id,
            "name": row.name,
            "city_id": row.city_id,
            "user_id": row.user_id,
            "is_active": row.is_active,
            "soft_delete": row.soft_delete,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
        }
        for row in result
    ]

    response = BaseResponse(
        message={'field': '', 'message': 'get all authors successfully'},
        data=data
    )
    return response
