from django.shortcuts import render
from .models import Course, Lesson, StudentCourse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .serializers import CourseSerializer, LessonSerializer, StudentAddCourseSerializer


class CourseAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonAPIView(ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_slug']
        return Lesson.objects.filter(course__slug=course_id)


class StudentAddCourseView(CreateAPIView):
    queryset = StudentCourse
    serializer_class = StudentAddCourseSerializer
