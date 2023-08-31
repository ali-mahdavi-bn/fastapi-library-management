from sqlalchemy import text
from sqlalchemy.orm import Session

from database.database import engine
from schemas.BaseResponse import BaseResponse


def view_gerne() -> BaseResponse:
    with Session(bind=engine) as session:
        result = session.execute(text("SELECT id, name, is_active, soft_delete, created_at, updated_at FROM genres WHERE is_active = TRUE and soft_delete = FALSE"))
        data = [
            {
                "id": row.id,
                "name": row.name,
                "is_active": row.is_active,
                "soft_delete": row.soft_delete,
                "created_at": row.created_at,
                "updated_at": row.updated_at,
            }
            for row in result
        ]

    response = BaseResponse(
        message={'field': '', 'message': 'get all genre successfully'},
        data=data
    )
    return response
