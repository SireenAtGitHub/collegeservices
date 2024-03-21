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
