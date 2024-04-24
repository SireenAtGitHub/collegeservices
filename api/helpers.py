from rest_framework.response import Response
from rest_framework.status import *


SEMESTER_DATA_RETRIEVED = "Semester data retrieved successfully."
SUBJECT_DATA_RETRIEVED = "Subject data retrieved successfully."
SUBJECT_NOT_FOUND = "We couldn't locate the subject '{0}' you requested."
SUBJECT_CREATED = "Subject created successfully."
SUBJECT_UPDATED = "Subject updated successfully."
NON_INT_FIELD = ["A valid integer is required."]
TEACHER_NOT_FOUND = "Teacher Not Found"
TEACHER_NOT_FOUND_MESSAGE = (
    "The email ID you provided does not correspond to an existing user in our system."
)
TEACHER_LOGIN_MESSAGE = "Teacher session initiated."


class ResponseHelper:
    def response(
        self, message=None, data=None, errors=None, status=HTTP_200_OK
    ) -> Response:
        response = {
            "status": status,
            "data": data,
            "message": message,
            "errors": errors,
        }
        return Response(response, status=status)


class ValidationHelper:
    def validate_int(self, value, field="id"):
        if not str(value).isdigit():
            return ResponseHelper.response(
                self,
                errors={field: NON_INT_FIELD},
                status=HTTP_400_BAD_REQUEST,
            )
