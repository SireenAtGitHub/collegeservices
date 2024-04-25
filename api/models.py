from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Semester(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    semester = models.ForeignKey(Semester, on_delete=models.DO_NOTHING, default=None)


class Subject(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(5)])
    code = models.CharField(
        max_length=10, unique=True, validators=[MinLengthValidator(4)]
    )
    semester = models.ForeignKey(
        Semester, on_delete=models.DO_NOTHING, related_name="subjects"
    )

    def __str__(self) -> str:
        return self.name
