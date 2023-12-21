from django.urls import path
from .views import CourseAPIView

urlpatterns = [
    path('courses/', CourseAPIView.as_view())
]
