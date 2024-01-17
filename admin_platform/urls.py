from django.urls import path
from .views import AddCourseAPI

urlpatterns = [
    path('add_course/', AddCourseAPI.as_view()),
]

