from rest_framework.generics import GenericAPIView
from .models import *
from .serializers import *
from .helpers import *
from rest_framework.parsers import FormParser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from rest_framework.decorators import api_view


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class TeacherLoginView(GenericAPIView, ResponseHelper):
    parser_classes = [FormParser]

    def post(self, request):
        serializer = TeacherLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get("email")
            password = request.data.get("password")
            user = authenticate(username=email, password=password)
            if user:
                token_data = get_tokens_for_user(user=user)
                return self.response(data=token_data, message=TEACHER_LOGIN_MESSAGE)
            else:
                return self.response(
                    errors=TEACHER_NOT_FOUND,
                    message=TEACHER_NOT_FOUND_MESSAGE,
                    status=HTTP_404_NOT_FOUND,
                )
        else:
            return self.response(errors=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def teacher_exists(request):
    serializer = TeacherLoginSerializer(data=request.data)
    if serializer.is_valid():
        try:
            User.objects.get(username=request.data["email"])
            return ResponseHelper.response(data={"exists": True})
        except User.DoesNotExist:
            return ResponseHelper.response(
                data={"exists": False},
                errors=TEACHER_NOT_FOUND,
                message=TEACHER_NOT_FOUND_MESSAGE,
                status=HTTP_404_NOT_FOUND,
            )
    else:
        return ResponseHelper.response(
            errors=serializer.errors, status=HTTP_400_BAD_REQUEST
        )


class SemesterView(GenericAPIView, ResponseHelper):
    def get(self, request):
        params = request.query_params
        if "id" in params:
            id = params.get("id")
            semester_serializer = SemesterSerializer(data={"id": id})
            if semester_serializer.is_valid():
                obj = Semester.objects.get(id=id)
                serializer = SemesterSubjectSerilaizer(obj)
                for subject in serializer.data.get("subjects", []):
                    subject.pop("semester")
                return self.response(
                    data={"semester": serializer.data}, message=SEMESTER_DATA_RETRIEVED
                )
            return self.semester_not_available(semester_serializer.errors)
        else:
            objects = Semester.objects.all()
            serializer = SemesterSubjectSerilaizer(objects, many=True)
            for semester in serializer.data:
                for subject in semester.get("subjects", []):
                    subject.pop("semester")
            return self.response(
                data={"count": len(serializer.data), "semesters": serializer.data},
                message=SEMESTER_DATA_RETRIEVED,
            )


class SubjectView(GenericAPIView, ResponseHelper, ValidationHelper):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        if "code" not in request.query_params:
            objects = Subject.objects.all()
            serializer = SubjectSerializer(objects, many=True)
            return self.response(
                data={"count": len(serializer.data), "subjects": serializer.data},
                message=SUBJECT_DATA_RETRIEVED,
            )
        else:
            code = request.query_params.get("code")
            try:
                object = Subject.objects.get(code=code)
                serializer = SubjectSerializer(object)
                return self.response(
                    data={"subject": serializer.data}, message=SUBJECT_DATA_RETRIEVED
                )
            except Subject.DoesNotExist:
                return self.response(
                    errors=SUBJECT_NOT_FOUND.format(code), status=HTTP_404_NOT_FOUND
                )

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.response(
                message=SUBJECT_CREATED, data=serializer.data, status=HTTP_201_CREATED
            )
        else:
            return self.semester_not_available(errors=serializer.errors)

    def patch(self, request):
        id = request.data.get("id")
        response = self.validate_int(id)
        if response:
            return response
        try:
            subject = Subject.objects.get(id=id)
            serializer = SubjectSerializer(
                data=request.data, instance=subject, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return self.response(message=SUBJECT_UPDATED, data=serializer.data)
            return self.response(errors=serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Subject.DoesNotExist:
            pass
        return self.response(
            errors=SUBJECT_NOT_FOUND.format(id), status=HTTP_404_NOT_FOUND
        )


class StudentView(GenericAPIView, ResponseHelper, ValidationHelper):
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "email"]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        params = request.query_params
        # Error Validation - 'id' present, 'semester' present, 'search' present
        if len(params) > 1:
            return self.response(
                status=HTTP_400_BAD_REQUEST,
                message={"allowed_values": ["id", "semester", "search"]},
                errors=SEND_EITHER_FIELD.format("id' or 'search", "semester"),
            )

        # Fetch Student(s) with name or email - 'id' not present, 'semester' not present, 'search' present
        if "search" in params and "id" not in params and "semester" not in params:
            students = self.filter_queryset(Student.objects.all())
            serializer = StudentSerializer(students, many=True)
            return self.response(
                data={"count": len(serializer.data), "students": serializer.data},
                message=STUDENT_LIST_RETRIEVED,
            )

        # Fetch All Students - 'id' not present, 'semester' not present
        if "id" not in params and "semester" not in params:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return self.response(
                data={"count": len(serializer.data), "students": serializer.data},
                message=STUDENT_LIST_RETRIEVED,
            )

        # Fetch only single student - 'id' present, 'semester' not present
        if "id" in params and "semester" not in params:
            id = params.get("id")
            response = self.validate_int(id)
            if response:
                return response
            try:
                student = Student.objects.get(id=id)
                serializer = StudentSerializer(student)
                return self.response(
                    data={"student": serializer.data}, message=STUDENT_RETRIEVED
                )
            except Student.DoesNotExist:
                return self.response(
                    message=STUDENT_NOT_FOUND.format(id), status=HTTP_404_NOT_FOUND
                )

        # Fetch Student(s) with semester - 'id' not present, 'semester' present
        if "semester" in params and "id" not in params:
            id = params.get("semester")
            response = self.validate_int(id, "semester")
            if response:
                return response
            try:
                semester_serializer = SemesterSerializer(
                    data={"id": id, "name": "string"}
                )
                semester_serializer.is_valid()
                semester = Semester.objects.get(id=id)
                students = Student.objects.filter(semester=id)
                serializer = StudentSerializer(students, many=True)
                count = len(serializer.data)
                semester = {"id": int(id), "name": semester.name}
                for student in serializer.data:
                    semester = student.pop("semester")
                semester["count"] = count
                semester["students"] = serializer.data
                return self.response(
                    data={"semester": semester},
                    message=STUDENT_LIST_RETRIEVED,
                )
            except Semester.DoesNotExist:
                return self.semester_not_available(semester_serializer.errors)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.response(
                message=STUDENT_CREATED, data=serializer.data, status=HTTP_201_CREATED
            )
        else:
            return self.semester_not_available(serializer.errors)

    def delete(self, request):
        data = request.data
        serializer = DeleteStudentsSerializer(data=data)
        if serializer.is_valid():
            for student in serializer.data.get("students", []):
                object = Student.objects.get(id=student)
                object.delete()
            return self.response(data=serializer.data, message=STUDENT_DELETED)
        else:
            return self.response(errors=serializer.errors, status=HTTP_400_BAD_REQUEST)


class StudentSemesterView(GenericAPIView, ResponseHelper):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def patch(self, request):
        data = request.data
        semester_id = data.get("id")
        serializer = StudentSemesterSerializer(data=data)
        if serializer.is_valid():
            semester = Semester.objects.get(id=semester_id)
            for student in serializer.data.get("students", []):
                object = Student.objects.get(id=student)
                object.semester = semester
                object.save()
            return self.response(data=serializer.data, message=SEMESTER_UPDATED)
        error = serializer.errors.get("id")
        if error is not None:
            if error[0] == f""""{semester_id}" is not a valid choice.""":
                return self.semester_not_available(serializer.errors)
        return self.response(errors=serializer.errors, status=HTTP_400_BAD_REQUEST)
