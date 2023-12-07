from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Student
from .serializers import UserSerializer, StudentSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(user)
        # staff = Student.objects.filter(user=user)
        # token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)  # Выводим данные в консоль
        response = super().post(request, *args, **kwargs)
        print(response.data)  # Выводим ответ в консоль
        return response


class RegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save()
            student_data = {**request.data, 'user': user.id}
            student_serializer = StudentSerializer(data=student_data)

            if student_serializer.is_valid():
                student_serializer.save()
                return Response(student_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Invalid student data', 'errors': student_serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Invalid user data', 'errors': user_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
