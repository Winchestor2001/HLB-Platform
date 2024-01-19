from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Lesson, Article, Quiz
from .serializers import AddCourseSerializer, GetCourseSerializer, AddLessonSerializer


class AddCourseAPI(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = AddCourseSerializer


class GetCoursesAPI(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = GetCourseSerializer


class AddLessonAPI(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = AddLessonSerializer


class DeleteCourseAPI(DestroyAPIView):
    queryset = Course.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.delete()
        return Response(status=204)


class DeleteLessonAPI(DestroyAPIView):
    queryset = Lesson.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.delete()
        return Response(status=204)

