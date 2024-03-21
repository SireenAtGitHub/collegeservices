from rest_framework import serializers
from .models import *


class SemesterSerializer(serializers.Serializer):
    id = serializers.ChoiceField(
        choices=Semester.objects.all().values_list("id", flat=True), required=False
    )
    name = serializers.CharField(max_length=100, required=False)


class SubjectSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()

    class Meta:
        model = Subject
        fields = "__all__"


class SemesterSubjectSerilaizer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Semester
        fields = ["id", "name", "subjects"]
