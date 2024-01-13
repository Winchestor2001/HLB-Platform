from .models import Course, Lesson, StudentCourse, StudentLesson, Article
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from .serializers import CourseSerializer, LessonSerializer, StudentAddCourseSerializer, StudentCoursesSerializer, \
    StudentLessonSerializer, ArticleSerializer, StudentArticleSerializer
from rest_framework.permissions import IsAuthenticated


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
        return StudentLesson.objects.filter(course__slug=course_id)


class StudentArticleAPIView(RetrieveAPIView):
    serializer_class = StudentArticleSerializer
    lookup_field = 'slug'
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     article_id = self.kwargs['article_id']
    #     return Article.objects.get(pk=article_id)

