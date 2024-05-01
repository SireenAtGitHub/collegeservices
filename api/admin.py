from .models import Semester, Subject
from django.contrib import admin

admin.site.site_title = "College Services"
admin.site.site_header = "College Services Admin"
admin.site.index_title = "College Services administration"


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code", "semester"]
