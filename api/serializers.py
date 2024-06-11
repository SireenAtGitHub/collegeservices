from rest_framework import serializers
from .models import *
from .helpers import *


class TeacherLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"read_only": True}}


class SemesterSerializer(serializers.Serializer):
    id = serializers.ChoiceField(
        choices=Semester.objects.all().values_list("id", flat=True), required=True
    )
    name = serializers.CharField(max_length=100, required=False)


class SubjectSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()

    teacher_first_name = serializers.ReadOnlyField(source="teacher.first_name")
    teacher_last_name = serializers.ReadOnlyField(source="teacher.last_name")

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
        fields = "__all__"

    def create(self, validated_data):
        semester = validated_data.pop("semester")
        serializer = SemesterSerializer(semester)
        student = Student.objects.create(
            id=None, semester_id=serializer.data.get("id"), **validated_data
        )
        return student

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.name)
        try:
            semester_id = validated_data["semester"]["id"]
            instance.semester = Semester.objects.get(id=semester_id)
        except:
            pass
        instance.save()
        return instance


class DeleteStudentsSerializer(serializers.Serializer, ValidationHelper):
    students = serializers.ListField(child=serializers.IntegerField())

    def validate_students(self, value):
        invalid_students = self.verify_students(value)
        if invalid_students:
            raise serializers.ValidationError(
                {"message": STUDENTS_NOT_FOUND, "students": invalid_students}
            )
        return value


class StudentSemesterSerializer(serializers.Serializer, ValidationHelper):
    id = serializers.ChoiceField(
        choices=Semester.objects.all().values_list("id", flat=True), required=True
    )
    students = serializers.ListField(child=serializers.IntegerField())

    def validate_students(self, value):
        invalid_students = self.verify_students(value)
        if invalid_students:
            raise serializers.ValidationError(
                {"message": STUDENTS_NOT_FOUND, "students": invalid_students}
            )
        return value


class MarksSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    marks = serializers.IntegerField(required=True)


class StudentMarksSerializer(serializers.Serializer, ValidationHelper):
    subject = serializers.ChoiceField(
        choices=Subject.objects.all().values_list("code", flat=True), required=True
    )
    students = serializers.ListSerializer(child=MarksSerializer(), min_length=1)

    def validate(self, data):
        students = [sub["id"] for sub in data["students"]]
        invalid_students = self.verify_students(students)
        if invalid_students:
            raise serializers.ValidationError(
                {"message": STUDENTS_NOT_FOUND, "students": invalid_students}
            )
        invalid_students = []
        for student in data["students"]:
            student_obj = Student.objects.get(id=student["id"])
            subject_obj = Subject.objects.get(code=data["subject"])
            if student_obj.semester_id != subject_obj.semester_id:
                invalid_students.append(student["id"])
        if invalid_students:
            raise serializers.ValidationError(
                {"message": SUBJECT_STUDENT_NOT_MATCHED, "students": invalid_students}
            )
        return data

    def create(self, validated_data):
        subject = Subject.objects.get(code=validated_data["subject"])
        for student in validated_data["students"]:
            try:
                marks = Marks.objects.get(subject=subject.id, student=student["id"])
                marks.marks = student["marks"]
                marks.save()
            except Marks.DoesNotExist:
                marks = Marks.objects.create(
                    subject_id=subject.id,
                    marks=student["marks"],
                    student_id=student["id"],
                )
                marks.save()
        return object
