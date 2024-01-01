from django.urls import path
from .views import CourseAPIView, LessonAPIView, StudentAddCourseView, StudentCoursesView, StudentLessonAPIView

urlpatterns = [
    path('courses/', CourseAPIView.as_view()),
    path('lessons/<slug:course_slug>/', LessonAPIView.as_view()),
    path('add_course/', StudentAddCourseView.as_view()),
    path('student_courses/<int:student_id>/', StudentCoursesView.as_view()),
    path('student_lessons/<slug:course_slug>/', StudentLessonAPIView.as_view()),
]
