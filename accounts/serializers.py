from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = Student
        fields = "__all__"
