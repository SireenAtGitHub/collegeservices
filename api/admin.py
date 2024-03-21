from .models import Semester, Subject
from django.contrib import admin


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
