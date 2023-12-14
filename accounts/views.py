from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Student
from .serializers import UserSerializer, StudentSerializer
from drf_yasg.utils import swagger_auto_schema

from .yasg_scheme import registration_post_scheme, registration_post_request


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        student = Student.objects.filter(user=user)
        if student.exists():
            token['full_name'] = student[0].full_name
            token['phone_number'] = student[0].full_name

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class RegistrationAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get doctors list (web)",
        responses={200: registration_post_scheme},
        request_body=registration_post_request
    )
    def post(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save()
            student_data = {**request.data, 'user': user.id}
            student_serializer = StudentSerializer(data=student_data)

            if student_serializer.is_valid():
                student_serializer.save()
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                response_data = {
                    'access_token': access_token,
                    'refresh_token': str(refresh),
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Invalid student data', 'errors': student_serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Invalid user data', 'errors': user_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
