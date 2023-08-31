from datetime import datetime

from pydantic import BaseModel

from schemas.AuthorsSchemas import AuthorOut
from schemas.BooksSchemas import BookOut
from schemas.BrowingSchemas import BorrowingOut
from schemas.UserSchemas import UserOut


class BaseResponse(BaseModel):
    success: bool = True
    message: dict
    data: list
    time: str = str(datetime.now())
    v: int = 1


class BaseResponseUser(BaseResponse):
    data: UserOut


class BaseResponseBook(BaseResponse):
    data: BookOut


class BaseResponseAuthor(BaseResponse):
    data: AuthorOut


class BaseResponseBorrowing(BaseResponse):
    data: BorrowingOut


def validate_response(filed: str , errors: dict) -> dict:
    return {'field': filed, 'message': {
        "errors": errors
    }}
