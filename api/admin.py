from .models import Semester, Subject
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code", "semester"]
