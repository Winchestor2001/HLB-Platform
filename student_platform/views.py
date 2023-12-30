from django.shortcuts import render
from .models import Course, Lesson, StudentCourse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .serializers import CourseSerializer, LessonSerializer, StudentAddCourseSerializer
from rest_framework.permissions import IsAuthenticated


class CourseAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class LessonAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_slug']
        return Lesson.objects.filter(course__slug=course_id)


class StudentAddCourseView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = StudentCourse
    serializer_class = StudentAddCourseSerializer


class StudentCoursesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentAddCourseSerializer

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        queryset = StudentCourse.objects.filter(student__id=student_id)
        return queryset
