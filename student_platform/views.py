from rest_framework import status
from rest_framework.response import Response

from accounts.models import Student
from click_payment.models import PaymentInvoice
from click_payment.serializers import PaymentInvoiceSerializer
from .utils import check_student_quizzes, filter_student_courses
from admin_platform.models import Quiz
from .models import Course, Lesson, StudentCourse, StudentLesson, Article, StudentArticle, StudentQuiz, \
    StudentSingleArticle
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from .serializers import CourseSerializer, LessonSerializer, StudentAddCourseSerializer, StudentCoursesSerializer, \
    StudentLessonSerializer, StudentArticleSerializer, StudentArticleQuizSerializer, \
    StudentQuizSerializer, GetAllArticlesSerializer, StudentSingleSerializer
from rest_framework.permissions import IsAuthenticated
from random import shuffle
from django.db.models import Q
from environs import Env
from rest_framework.reverse import reverse

env = Env()
env.read_env()


class CourseAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     student = Student.objects.get(user=self.request.user)
    #     student_courses = StudentCourse.objects.filter(student=student).values_list('course__slug', flat=True)
    #     return Course.objects.exclude(slug__in=student_courses)


class LessonAPIView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['course_slug']
        return Lesson.objects.filter(course__slug=course_id)


class StudentAddCourseView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        student = Student.objects.get(id=request.data['student'])
        course_slug = request.data['course']
        student_course = Course.objects.get(slug=course_slug)

        if student_course.paid:
            payment_data = PaymentInvoice.objects.create(
                payer=student, service=student_course.pk, type="course", amount=student_course.price
            )
            payment_data_serializer = PaymentInvoiceSerializer(instance=payment_data)

            response_data = {
                'success': True,
                'message': 'Invoice created successfully.',
                'invoice': self.create_invoice(request, payment_data_serializer.data),
                'course_name': student_course.title,
                'course_price': student_course.price,
                'is_certificate': student_course.certification,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            serializer = StudentAddCourseSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create_invoice(self, request, data):
        url = (
            f"https://my.click.uz/services/pay?service_id={env.str('CLICK_SERVICE_ID')}"
            f"&merchant_id={env.str('CLICK_MERCHANT_ID')}&amount={data.get('amount')}"
            f"&transaction_param={data.get('id')}"
            f"&return_url={reverse('status_invoice', request=request)}"
        )
        return url
    

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
        article = Article.objects.get(id=request.data['article_id'])
        student = Student.objects.get(user=request.user)
        student_quiz = StudentQuiz.objects.filter(student=student, score__lt=1).exclude(student__in=article.quiz.all())
        serializer = StudentQuizSerializer(student_quiz, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        quizzes = request.data
        incorrect_quizzes = check_student_quizzes(request.user, quizzes)
        return Response({"incorrect": incorrect_quizzes}, status=status.HTTP_200_OK)


class GetAllArticlesAPIView(ListAPIView):
    serializer_class = GetAllArticlesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        articles = Article.objects.all()
        if query:
            articles = Article.objects.filter(title__icontains=query)
        return articles


class StudentAddSingleArticleAPIView(CreateAPIView):
    queryset = StudentSingleArticle
    serializer_class = StudentSingleSerializer
    permission_classes = [IsAuthenticated]


class StudentSingleArticleAPIView(ListAPIView):
    serializer_class = StudentSingleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = StudentSingleArticle.objects.filter(student__user=user)
        return queryset

