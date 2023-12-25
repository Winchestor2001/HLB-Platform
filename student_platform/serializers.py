from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Course, Lesson, Article


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


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
        fields = ['id', 'title', 'poster_image', 'total_lessons']

    @staticmethod
    def get_total_lessons(obj):
        return obj.lesson_set.count()
