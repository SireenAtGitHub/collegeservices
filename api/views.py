from rest_framework.generics import GenericAPIView
from .models import *
from .serializers import *
from .helpers import *

ALL_SEMESTERS = Semester.objects.all().values_list("id", flat=True)


class SemesterView(GenericAPIView, ResponseHelper):
    def get(self, request):
        params = request.query_params
        if "id" in params:
            id = params.get("id")
            semester_serializer = SemesterSerializer(data={"id": id})
            if semester_serializer.is_valid():
                obj = Semester.objects.get(id=id)
                serializer = SemesterSubjectSerilaizer(obj)
                return self.response(
                    data={"semester": serializer.data}, message=SEMESTER_DATA_RETRIEVED
                )
            return self.response(
                errors=semester_serializer.errors,
                message={"available_semesters": ALL_SEMESTERS},
                status=HTTP_404_NOT_FOUND,
            )
        else:
            objects = Semester.objects.all()
            serializer = SemesterSubjectSerilaizer(objects, many=True)
            return self.response(
                data={"count": len(serializer.data), "semesters": serializer.data},
                message=SEMESTER_DATA_RETRIEVED,
            )


class SubjectView(GenericAPIView, ResponseHelper, ValidationHelper):
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
            return self.response(
                errors=serializer.errors,
                message={"available_semesters": ALL_SEMESTERS},
                status=HTTP_400_BAD_REQUEST,
            )

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
