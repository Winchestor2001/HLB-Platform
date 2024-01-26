from django.db.models.signals import post_delete
from django.dispatch import receiver
from admin_platform.models import Article


@receiver(post_delete, sender=Article)
def update_article_numbers_on_delete(sender, instance, **kwargs):
    lesson = instance.lesson
    remaining_articles = Article.objects.filter(lesson=lesson).order_by('number')

    for index, article in enumerate(remaining_articles, start=1):
        article.number = index
        article.save()
