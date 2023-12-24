from django.urls import path
from .views import CourseAPIView, LessonAPIView

urlpatterns = [
    path('courses/', CourseAPIView.as_view()),
    path('lessons/<int:course_id>/', LessonAPIView.as_view()),
]
