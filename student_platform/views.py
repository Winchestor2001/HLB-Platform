from django.shortcuts import render
from .models import Course, Lesson
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import CourseSerializer, LessonSerializer


class CourseAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonAPIView(ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lesson.objects.filter(course__id=course_id)
