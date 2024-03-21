from django.urls import path
from .views import *


urlpatterns = [
    path("semester", SemesterView.as_view()),
    path("subject", SubjectView.as_view()),
]
