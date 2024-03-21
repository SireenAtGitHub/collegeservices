from rest_framework.response import Response
from rest_framework.status import *


SEMESTER_DATA_RETRIEVED = "Semester data retrieved successfully."


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
