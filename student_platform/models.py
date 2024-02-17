from django.db import models
from accounts.models import Student
from admin_platform.models import Course, Lesson, Quiz, Article


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, to_field='slug')

    def __str__(self):
        return f"{self.student} - {self.course}"


class StudentLesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.lesson}"


class StudentArticle(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)
    lock = models.BooleanField(default=True)
    finished = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.article}"


class StudentQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(StudentArticle, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student} - {self.quiz}"


class StudentSingleArticle(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.article}"
