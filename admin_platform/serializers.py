from rest_framework.serializers import ModelSerializer
from .models import Course, Lesson, Article, Quiz


class AddCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
