from django.db import models
from accounts.models import Student


class Course(models.Model):
    slug = models.SlugField(blank=True, null=True, unique=True)
    title = models.CharField(max_length=200)
    poster_image = models.ImageField(upload_to='course/')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    number = models.IntegerField()
    title = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course} - {self.title}"


class Quiz(models.Model):
    option = models.CharField(max_length=150)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=100)
    mark_1 = models.CharField(max_length=100)
    mark_2 = models.CharField(max_length=100)
    mark_3 = models.CharField(max_length=100)
    mark_4 = models.CharField(max_length=100)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.question} - {self.score}"


class Article(models.Model):
    number = models.IntegerField(default=0)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    context = models.TextField()
    file = models.FileField(upload_to='article/file/', blank=True, null=True)
    video = models.FileField(upload_to='article/video/', blank=True, null=True)
    image = models.FileField(upload_to='article/image/', blank=True, null=True)
    quiz = models.ManyToManyField(Quiz)
    read_time = models.BigIntegerField()

    def __str__(self):
        return f"{self.lesson} - {self.title}"


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, to_field='slug', unique=True)

    def __str__(self):
        return f"{self.student} - {self.course}"


class StudentLesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE, null=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.lesson}"


class StudentArticle(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    lesson = models.ForeignKey(StudentLesson, on_delete=models.CASCADE, null=True)
    lock = models.BooleanField(default=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.article}"

