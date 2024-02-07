from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from admin_platform.models import Course


class HomePageView(ListView):
    queryset = Course.objects.all()
    template_name = 'index.html'
    context_object_name = 'courses'
