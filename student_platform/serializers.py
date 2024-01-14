from rest_framework.serializers import ModelSerializer, SerializerMethodField

from accounts.models import Student
from .models import Course, Lesson, Article, Quiz, StudentCourse, StudentLesson, StudentArticle
from .utils import filter_student_lessons


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

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
        for lesson in lessons:
            StudentLesson.objects.create(
                lesson=lesson, student=student, course=course
            )

            articles = Article.objects.filter(lesson=lesson)

            for article in articles:
                if article.number != 1:
                    lock = True
                else:
                    lock = False

                StudentArticle.objects.create(
                    lesson=lesson, student=student, lock=lock, article=article
                )

        return super(StudentAddCourseSerializer, self).create(validated_data)


class StudentCoursesSerializer(ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = '__all__'

    @staticmethod
    def count_articles(obj):
        lessons = StudentLesson.objects.filter(course=obj.course)
        finished_articles = StudentLesson.objects.filter(course=obj.course, finished=True).count()
        total_articles = 0
        for lesson in lessons:
            total_articles += StudentArticle.objects.filter(lesson=lesson.lesson).count()

        return finished_articles * 100 // total_articles

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        data['poster_image'] = request.build_absolute_uri(instance.course.poster_image.url)
        data['slug'] = instance.course.slug
        data['title'] = instance.course.title
        data['statistic_bar'] = self.count_articles(instance)
        return data


class InnerStudentArticleSerializer(ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = StudentArticle
        fields = '__all__'


class StudentArticleSerializer(ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = StudentArticle
        fields = '__all__'


class InnerLessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title']


class StudentLessonSerializer(ModelSerializer):

    class Meta:
        model = StudentLesson
        fields = '__all__'

    def get_lesson_articles(self, obj):
        user = self.context['request'].user
        result = InnerStudentArticleSerializer(instance=StudentArticle.objects.filter(lesson=obj.lesson, student__user=user), many=True)
        return result.data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['lesson_articles'] = filter_student_lessons(self.get_lesson_articles(instance))
        data['title'] = InnerLessonSerializer(instance=instance.lesson).data.get('title')
        return data


class QuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class StudentArticleQuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
