import jwt
from django.conf import settings

from accounts.models import Student
from admin_platform.models import Quiz
from student_platform.models import StudentQuiz


def decode_jwt_token(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token:
        jwt_token = request.headers['Authorization'].split()[-1]
        return jwt.decode(jwt_token, settings.SECRET_KEY, 'HS256')['username']
    return None


def check_student_quizzes(user, quizzes):
    for quiz in quizzes:
        db_quiz = Quiz.objects.get(id=quiz['quiz_id'])
        score = 0
        if db_quiz.answer == quiz['variant']:
            score = db_quiz.score

        student = Student.objects.get(user=user)
        StudentQuiz.objects.create(
            student=student, quiz=db_quiz, score=score
        )


