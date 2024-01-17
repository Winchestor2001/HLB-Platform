from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Lesson, Article, Quiz
from .serializers import AddCourseSerializer


class AddCourseAPI(APIView):
    # queryset = Course.objects.all()
    # serializer_class = AddCourseSerializer
    def post(self, request):
        print(request.data)
        return Response({'status': "ok"})
