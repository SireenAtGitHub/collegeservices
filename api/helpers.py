from rest_framework.response import Response
from rest_framework.status import *
from .models import Student


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
SEND_EITHER_FIELD = (
    "Invalid request format. Please send either '{0}' or '{1}' in the request."
)
STUDENT_CREATED = "Student created successfully."
STUDENT_RETRIEVED = "Student retrieved successfully."
SEMESTER_UPDATED = "Semester updated for given student(s)."
STUDENT_DELETED = "Student(s) deleted successfully."
STUDENT_LIST_RETRIEVED = "List of students retieved successfully."
STUDENT_NOT_FOUND = "Student with Id {0} not found."
SEMESTER_STUDENT_NOT_FOUND = "Students with semester {0} not found."


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

    def verify_students(self, students):
        invalid_students = []
        for student in students:
            try:
                Student.objects.get(id=student)
            except Student.DoesNotExist:
                invalid_students.append(student)
        return invalid_students
