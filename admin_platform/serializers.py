from django.template.defaultfilters import slugify
from rest_framework.serializers import ModelSerializer
from .models import Course, Lesson, Article, Quiz


class AddCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return Course.objects.create(**validated_data)
