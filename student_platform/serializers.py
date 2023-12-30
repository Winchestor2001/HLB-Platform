from rest_framework.serializers import ModelSerializer, SerializerMethodField

from accounts.models import Student
from .models import Course, Lesson, Article, Quiz, StudentCourse, StudentLesson, StudentArticle


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['quiz_score'] = sum(list(instance.quiz.values_list('score', flat=True)))
        return data


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'number', 'title', 'price', 'paid']

    @staticmethod
    def get_lesson_articles(obj):
        result = ArticleSerializer(instance=obj.article_set.all(), many=True)
        return result.data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['lesson_articles'] = self.get_lesson_articles(instance)
        return data


class CourseSerializer(ModelSerializer):
    total_lessons = SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'slug', 'title', 'poster_image', 'total_lessons']

    @staticmethod
    def get_total_lessons(obj):
        return obj.lesson_set.count()


class StudentAddCourseSerializer(ModelSerializer):

    class Meta:
        model = StudentCourse
        fields = '__all__'

    def create(self, validated_data):
        student = validated_data['student']
        course = validated_data['course']
        lessons = Lesson.objects.filter(course=course)
        student_course = StudentCourse.objects.create(
                student=student, course=course, slug=course.slug
        )
        for lesson in lessons:
            article = Article.objects.get(lesson=lesson)
            student_lesson = StudentLesson.objects.create(
                course=student_course, student=student, lesson=lesson
            )

            if lesson.number == 1:
                lock = True
            else:
                lock = False

            StudentArticle.objects.create(
                article=article, student=student, lock=lock, lesson=student_lesson
            )

        return validated_data