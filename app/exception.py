from rest_framework.exceptions import APIException
from rest_framework import status
class GenericException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    code = 600
    summary = "Error"
    error_detail = None

    def __init__(self, message=None, status_code=None, error_detail=None):
        print(message)
        if not message:
            message = "Oops! Something went wrong, please try again"
        if status_code:
            self.status_code = status_code
        if error_detail:
            self.error_detail = error_detail
        super().__init__(detail=message)

    def serialize(self):
        data = {
            "code": self.code,
            "summary": self.summary,
            "message": self.detail,
        }
        return data

class SignUpUserException(GenericException):
    code = 601

    def __init__(self, message=None):
        if not message:
            message = "This email is activated by other user"
        super().__init__(message=message)