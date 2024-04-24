from rest_framework import serializers
from .models import *


class SemesterSerializer(serializers.Serializer):
    id = serializers.ChoiceField(
        choices=Semester.objects.all().values_list("id", flat=True), required=True
    )
    name = serializers.CharField(max_length=100, required=False)


class SubjectSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()

    class Meta:
        model = Subject
        fields = "__all__"

    def create(self, validated_data):
        semester = validated_data.pop("semester")
        serializer = SemesterSerializer(semester)
        subject = Subject.objects.create(
            semester_id=serializer.data["id"], **validated_data
        )
        return subject

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.code = validated_data.get("code", instance.code)
        try:
            semester_id = validated_data["semester"]["id"]
            instance.semester = Semester.objects.get(id=semester_id)
        except:
            pass
        instance.save()
        return instance


class SemesterSubjectSerilaizer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Semester
        fields = ["id", "name", "subjects"]


class TeacherLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
