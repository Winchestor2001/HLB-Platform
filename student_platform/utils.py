from accounts.models import Student
from admin_platform.models import Quiz, Article
from student_platform.models import StudentQuiz, StudentArticle
from admin_platform.serializers import GetQuizSerializer


def filter_student_lessons(obj):
    result = []
    for item in obj:
        result.append(
            {
                'id': item['article']['id'],
                'slug': item['article']['slug'],
                'title': item['article']['title'],
                'quiz_score': item['article']['quiz_score'],
                'lock': item['lock'],
                'finished': item['finished'],
            }
        )
    return result


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
    pass_score = quizzes_score * 60 // 100
    if solved_quiz_score >= pass_score:
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


def filter_student_courses(obj):
    courses = []
    for item in obj:
        courses.append(item.course.slug)
    return courses


