from schemas.BaseResponse import BaseResponse


def custom_response(data, message):
    response = BaseResponse(
        message={'field': '', 'message': message},
        data=data
    )
    return response
