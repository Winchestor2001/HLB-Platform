from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Lesson, Article, Quiz
from .serializers import AddCourseSerializer, GetCourseSerializer, AddLessonSerializer, GetArticleSerializer, \
    AddArticleSerializer, AddQuizSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class AddCourseAPI(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = AddCourseSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class GetCoursesAPI(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = GetCourseSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class AddLessonAPI(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = AddLessonSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeleteCourseAPI(DestroyAPIView):
    queryset = Course.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.delete()
        return Response(status=204)


class DeleteLessonAPI(DestroyAPIView):
    queryset = Lesson.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.delete()
        return Response(status=204)


class UpdateCourseAPI(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = AddCourseSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAdminUser]


class UpdateLessonAPI(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = AddLessonSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAdminUser]


class GetArticleAPI(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = GetArticleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        course = Course.objects.get(id=self.request.GET.get('course_id'))
        lesson = Lesson.objects.get(id=self.request.GET.get('lesson_id'), course=course)
        return Article.objects.filter(lesson=lesson)


class AddArticleAPI(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = AddArticleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeleteArticleAPI(DestroyAPIView):
    queryset = Article.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.delete()
        return Response(status=204)


class UpdateArticleAPI(UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = AddArticleSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAdminUser]


class AddQuizAPI(CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = AddQuizSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]


class DeleteQuizAPI(DestroyAPIView):
    queryset = Quiz.objects.all()
    lookup_field = 'id'

    # permission_classes = [IsAuthenticated, IsAdminUser]
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.delete()
        return Response(status=204)


class UpdateQuizAPI(UpdateAPIView):
    queryset = Quiz.objects.all()
    lookup_field = 'id'
    serializer_class = AddQuizSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]
