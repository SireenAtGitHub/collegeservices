from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Semester(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=None)


class Subject(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(5)])
    code = models.CharField(
        max_length=10, unique=True, validators=[MinLengthValidator(4)]
    )
    semester = models.ForeignKey(
        Semester, on_delete=models.DO_NOTHING, related_name="subjects"
    )
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name


class Marks(models.Model):
    marks = models.PositiveIntegerField()
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
