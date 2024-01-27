from django.urls import path
from .views import AddCourseAPI, GetCoursesAPI, AddLessonAPI, DeleteCourseAPI, DeleteLessonAPI, UpdateCourseAPI, \
    UpdateLessonAPI, GetArticleAPI, AddArticleAPI, DeleteArticleAPI, UpdateArticleAPI

urlpatterns = [
    path('add_course/', AddCourseAPI.as_view()),
    path('get_courses/', GetCoursesAPI.as_view()),

    path('add_lesson/', AddLessonAPI.as_view()),

    path('delete_course/<int:id>/', DeleteCourseAPI.as_view()),
    path('delete_lesson/<int:id>/', DeleteLessonAPI.as_view()),

    path('update_course/<int:id>/', UpdateCourseAPI.as_view()),
    path('update_lesson/<int:id>/', UpdateLessonAPI.as_view()),

    path('get_articles/', GetArticleAPI.as_view()),
    path('add_article/', AddArticleAPI.as_view()),
    path('delete_article/<int:id>/', DeleteArticleAPI.as_view()),
    path('update_article/<int:id>/', UpdateArticleAPI.as_view()),
]
