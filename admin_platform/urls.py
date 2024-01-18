from django.urls import path
from .views import AddCourseAPI, GetCoursesAPI

urlpatterns = [
    path('add_course/', AddCourseAPI.as_view()),
    path('get_courses/', GetCoursesAPI.as_view()),
]

