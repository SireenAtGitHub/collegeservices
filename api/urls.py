from django.urls import path
from .views import SemesterView


urlpatterns = [
    path("semester", SemesterView.as_view()),
]
