from django.urls import path
from .views import CourseAPIView, LessonAPIView, StudentAddCourseView

urlpatterns = [
    path('courses/', CourseAPIView.as_view()),
    path('lessons/<slug:course_slug>/', LessonAPIView.as_view()),
    path('add_course/', StudentAddCourseView.as_view()),
]
