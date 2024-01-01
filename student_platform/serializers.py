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
        student_course = super(StudentAddCourseSerializer, self).create(validated_data)
        lessons = Lesson.objects.filter(course=course)
        for lesson in lessons:
            student_lesson = StudentLesson.objects.create(
                lesson=lesson, student=student, course=student_course
            )

            articles = Article.objects.filter(lesson=lesson)

            for article in articles:
                if article.number == 1:
                    lock = True
                else:
                    lock = False

                StudentArticle.objects.create(
                    lesson=student_lesson, student=student, lock=lock, article=article
                )

        return student_course


class StudentCoursesSerializer(ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = '__all__'

    @staticmethod
    def count_articles(obj):
        lessons = obj.studentlesson_set.all()
        finished_articles = 0
        total_articles = 0
        for lesson in lessons:
            finished_articles += lesson.studentarticle_set.filter(finished=True).count()
            total_articles += lesson.studentarticle_set.all().count()

        return finished_articles * 100 // total_articles

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        data['poster_image'] = request.build_absolute_uri(instance.course.poster_image.url)
        data['slug'] = instance.course.slug
        data['title'] = instance.course.title
        data['statistic_bar'] = self.count_articles(instance)
        return data


class StudentArticleSerializer(ModelSerializer):
    class Meta:
        model = StudentArticle
        fields = '__all__'


class StudentLessonSerializer(ModelSerializer):
    # lesson = LessonSerializer()

    class Meta:
        model = StudentLesson
        fields = '__all__'

    @staticmethod
    def get_lesson_articles(obj):
        result = StudentArticleSerializer(instance=obj.studentarticle_set.all(), many=True)
        return result.data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['lesson_articles'] = self.get_lesson_articles(instance)
        return data
