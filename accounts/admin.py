from django.contrib import admin

from student_platform.models import StudentLesson, StudentArticle
from .models import Student, Admin


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name']


@admin.register(StudentLesson)
class StudentLessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'lesson']


@admin.register(StudentArticle)
class StudentArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'article', 'lock']
