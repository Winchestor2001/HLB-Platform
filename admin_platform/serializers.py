from django.template.defaultfilters import slugify
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from .models import Course, Lesson, Article, Quiz


class AddCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        slug = slugify(validated_data['title'])
        if Course.objects.filter(slug=slug).exists():
            error_message = "Course with this title already exists."
            res = serializers.ValidationError(error_message)
            res.status_code = status.HTTP_409_CONFLICT
            raise res

        validated_data['slug'] = slug
        return Course.objects.create(**validated_data)


class GetCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        data = super(GetCourseSerializer, self).to_representation(instance)
        data['lessons'] = instance.lesson_set.all()
        return data
