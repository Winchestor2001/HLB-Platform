from django.contrib import admin
from .models import Course, Lesson, Article, Quiz, StudentCourse, StudentQuiz


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['id', 'title']
    list_display_links = ['title']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['number', 'course', 'title', 'price', 'paid']
    list_display_links = ['number', 'course']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['lesson', 'title', 'read_time']
    list_display_links = ['lesson']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['question', 'score']
    list_display_links = ['question']


@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ['student', 'course']
    list_display_links = ['student']


@admin.register(StudentQuiz)
class StudentQuizAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz']
    list_display_links = ['student']


