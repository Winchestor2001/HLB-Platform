from rest_framework import status
from rest_framework.response import Response

from accounts.models import Student
from admin_platform.models import Quiz
from .models import Course, Lesson, StudentCourse, StudentLesson, Article, StudentArticle, StudentQuiz
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from .serializers import CourseSerializer, LessonSerializer, StudentAddCourseSerializer, StudentCoursesSerializer, \
    StudentLessonSerializer, ArticleSerializer, StudentArticleSerializer, StudentArticleQuizSerializer, QuizSerializer, \
    StudentQuizSerializer
from rest_framework.permissions import IsAuthenticated
from random import shuffle


class CourseAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class LessonAPIView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['course_slug']
        return Lesson.objects.filter(course__slug=course_id)


class StudentAddCourseView(CreateAPIView):
    queryset = StudentCourse
    serializer_class = StudentAddCourseSerializer
    permission_classes = [IsAuthenticated]


class StudentCoursesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentCoursesSerializer

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        queryset = StudentCourse.objects.filter(student__id=student_id)
        return queryset


class StudentLessonAPIView(ListAPIView):
    serializer_class = StudentLessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['course_slug']
        user = self.request.user
        return StudentLesson.objects.filter(course__slug=course_id, student__user=user)


class StudentArticleAPIView(RetrieveAPIView):
    serializer_class = StudentArticleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_object(self):
        article_slug = self.kwargs['slug']
        user = self.request.user
        queryset = StudentArticle.objects.get(student__user=user, article__slug=article_slug)
        return queryset


class StudentArticleQuizAPIView(ListAPIView):
    serializer_class = StudentArticleQuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        article_slug = self.kwargs['slug']
        article = Article.objects.get(slug=article_slug)
        quizzes = list(article.quiz.all())
        shuffle(quizzes)
        return quizzes


class StudentArticleReadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        student = StudentArticle.objects.get(
            student__id=request.data['student_id'], article__slug=request.data['article_slug']
        )
        student.read = True
        student.save()
        return Response(status=status.HTTP_200_OK)


class StudentQuizAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = Student.objects.get(user=request.user)
        student_quiz = StudentQuiz.objects.filter(student=student, score__lt=1)
        serializer = StudentQuizSerializer(student_quiz, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        quiz_id = request.data['quiz_id']
        variant = request.data['variant']
        quiz = Quiz.objects.get(id=quiz_id)
        score = 0
        if quiz.answer == variant:
            score = quiz.score

        student = Student.objects.get(user=request.user)
        StudentQuiz.objects.create(
            student=student, quiz=quiz, score=score
        )
        return Response({"status": "RECEIVED"}, status=status.HTTP_200_OK)
