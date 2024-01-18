from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Lesson, Article, Quiz
from .serializers import AddCourseSerializer, GetCourseSerializer


class AddCourseAPI(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = AddCourseSerializer


class GetCoursesAPI(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = GetCourseSerializer

