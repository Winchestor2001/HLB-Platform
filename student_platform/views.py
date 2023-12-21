from django.shortcuts import render
from .models import Course
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import CourseSerializer


class CourseAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


