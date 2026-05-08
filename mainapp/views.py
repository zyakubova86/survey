from django.shortcuts import render

from .models import *


def home(request):
    if "/ru/" in request.path:
        template = 'mainapp/home_ru.html'
    else:
        template = 'mainapp/home_uz.html'

    return render(request, template)



def submit_survey(request):
    if "/ru/" in request.path:
        template = 'mainapp/survey_ru.html'
    else:
        template = 'mainapp/survey_uz.html'

    questions = Question.objects.filter(is_active=True).prefetch_related('options').order_by('order')
    departments = Department.objects.filter(is_active=True, name_uz__isnull=False, name_ru__isnull=False).exclude(name_uz='', name_ru='').order_by('name_uz')

    context = {
        'questions': questions,
        'departments': departments,
    }

    return render(request, template, context)



def thank_you(request):
    if "/ru/" in request.path:
        template = 'mainapp/thank_you_ru.html'
    else:
        template = 'mainapp/thank_you_uz.html'
    return render(request, template)
