from django.contrib import admin
from .models import Student, Admin


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name']
