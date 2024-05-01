from rest_framework import serializers
from .models import *
from .helpers import ValidationHelper

class TeacherLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {'password': {'read_only': True}}

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

class StudentSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()

    class Meta:
        model = Student
        fields = ["id", "name", "email", "semester"]

    def create(self, validated_data):
        semester = validated_data.pop("semester")
        serializer = SemesterSerializer(semester)
        student = Student.objects.create(
            id=None, semester_id=serializer.data.get("id"), **validated_data
        )
        return student


class DeleteStudentsSerializer(serializers.Serializer, ValidationHelper):
    students = serializers.ListField(child=serializers.IntegerField())

    def validate_students(self, value):
        invalid_students = self.verify_students(value)
        if invalid_students:
            raise serializers.ValidationError({"not_found": invalid_students})
        return value


class StudentSemesterSerializer(serializers.Serializer, ValidationHelper):
    id = serializers.ChoiceField(
        choices=Semester.objects.all().values_list("id", flat=True), required=True
    )
    students = serializers.ListField(child=serializers.IntegerField())

    def validate_students(self, value):
        invalid_students = self.verify_students(value)
        if invalid_students:
            raise serializers.ValidationError({"not_found": invalid_students})
        return value
