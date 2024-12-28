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
    list_display = ["id", "name", "code", "semester", "get_teacher", "image_icon"]

    @admin.display(ordering="teacher__first_name", description="Teacher Name")
    def get_teacher(self, obj):
        return f"{obj.teacher.first_name} {obj.teacher.last_name}"
