from django.urls import path
from .views import *


urlpatterns = [
    path("semester", SemesterView.as_view()),
    path("subject", SubjectView.as_view()),
    path("teacher/login", TeacherLoginView.as_view()),
    path("teacher/exists", teacher_exists),
    path("student", StudentView.as_view()),
    path("student/semester", StudentSemesterView.as_view()),
    path("student/marks", StudentsMarksView.as_view()),
]
