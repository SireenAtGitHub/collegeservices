from rest_framework.response import Response
from rest_framework.status import *
from .models import Student, Semester, Marks, Subject


ALL_SEMESTERS = Semester.objects.all().values_list("id", flat=True)


SEMESTER_DATA_RETRIEVED = "Semester data retrieved successfully."
SUBJECT_DATA_RETRIEVED = "Subject data retrieved successfully."
SUBJECT_NOT_FOUND = "We couldn't locate the subject '{0}' you requested."
SUBJECT_CREATED = "Subject created successfully."
SUBJECT_UPDATED = "Subject updated successfully."
NON_INT_FIELD = ["A valid integer is required."]
TEACHER_NOT_FOUND = "Teacher not found."
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
STUDENT_LIST_RETRIEVED = "List of students retrieved successfully."
STUDENT_NOT_FOUND = "Student with Id {0} not found."
SEMESTER_NOT_FOUND = "Semester with Id {0} not found."
SEMESTER_STUDENT_NOT_FOUND = "Students with semester {0} not found."
STUDENT_MARKS_UPDATED = "Marks updated successfully for given student(s)."
SUBJECT_STUDENT_NOT_MATCHED = (
    "One or more students have not been assigned the given subject."
)
STUDENTS_NOT_FOUND = "One or more students are not present in the directory."
RESULTS_NOT_UPDATED = "Results are not updated for one or more student."
STUDENT_UPDATED = "Student updated successfully."


class ResponseHelper:
    def response(
        self=None, message=None, data=None, errors=None, status=HTTP_200_OK
    ) -> Response:
        response = {
            "status": status,
            "data": data,
            "message": message,
            "errors": errors,
        }
        return Response(response, status=status)

    def semester_not_available(self, errors):
        return self.response(
            errors=errors,
            message={"available_semesters": ALL_SEMESTERS},
            status=HTTP_404_NOT_FOUND,
        )


class ResponseGeneratorHelper:
    def build_marksheet(self, student):
        id = student.id
        marks = {"id": int(id), "name": student.name, "marks": {}}
        marks_objects = Marks.objects.filter(student_id=id)
        subject_codes = Subject.objects.filter(semester_id=student.semester_id)
        for subject in subject_codes:
            marks["marks"][subject.code] = None
            for marks_object in marks_objects:
                if subject.semester_id == student.semester_id:
                    marks["marks"][marks_object.subject.code] = marks_object.marks
        return marks


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
