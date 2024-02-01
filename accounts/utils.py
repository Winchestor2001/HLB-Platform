import jwt
from django.conf import settings

from accounts.models import Student
from admin_platform.models import Quiz, Article
from student_platform.models import StudentQuiz, StudentArticle
from admin_platform.serializers import GetQuizSerializer


def decode_jwt_token(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token:
        jwt_token = request.headers['Authorization'].split()[-1]
        return jwt.decode(jwt_token, settings.SECRET_KEY, 'HS256')['username']
    return None


def check_student_quizzes(user, quizzes):
    article_slug = quizzes[-1]['articleSlug']
    quizzes_score = sum(item.score for item in Article.objects.get(slug=article_slug).quiz.all())
    article = StudentArticle.objects.get(student__user=user, article__slug=article_slug)
    solved_quiz_score = 0
    incorrect_quizzes = []
    saved_quizzes = []
    for quiz in quizzes[:-1]:
        db_quiz = Quiz.objects.get(id=quiz['quiz_id'])
        score = 0
        if db_quiz.answer == quiz['variant']:
            score = db_quiz.score
            solved_quiz_score += score
        else:
            incorrect_quizzes.append(
                GetQuizSerializer(instance=db_quiz).data
            )

        student = Student.objects.get(user=user)
        student_quiz = StudentQuiz.objects.create(
            student=student, quiz=db_quiz, score=score, article=article
        )
        saved_quizzes.append(student_quiz)

    if solved_quiz_score == quizzes_score:
        article.finished = True
        next_article = StudentArticle.objects.get(student__user=user, article__number=article.article.number+1)
        next_article.lock = False
        next_article.save()
    else:
        article.read = False
    article.save()

    for item in saved_quizzes:
        item.delete()

    return incorrect_quizzes

