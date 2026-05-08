from django.db import transaction
from django.shortcuts import render, redirect

from .models import *


def home(request):
    if "/ru/" in request.path:
        template = 'mainapp/home_ru.html'
    else:
        template = 'mainapp/home_uz.html'

    return render(request, template)


@transaction.atomic
def submit_survey(request):
    if "/ru/" in request.path:
        template = 'mainapp/survey_ru.html'
        redirect_url = 'thank_you_ru'
    else:
        template = 'mainapp/survey_uz.html'
        redirect_url = 'thank_you_uz'

    questions = Question.objects.filter(is_active=True).prefetch_related('options').order_by('order')
    departments = Department.objects.filter(is_active=True, name_uz__isnull=False, name_ru__isnull=False).exclude(name_uz='', name_ru='').order_by('name_uz')


    if request.method == 'POST':
        save_answers(request=request, questions=questions, departments=departments)
        return redirect(redirect_url)

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


def save_answers(request, questions, departments):

    submission = SurveySubmission.objects.create()

    answers = []

    for question in questions:
        field_name = f'question_{question.id}'

        # TEXT / NUMBER
        if question.question_type in ['text', 'number']:
            value = request.POST.get(field_name)

            if value:
                answers.append(Answer(submission=submission, question=question, text_answer=value)                )


        # SINGLE CHOICE
        elif question.question_type == 'single':
            value = request.POST.get(field_name)

            if not value:
                continue

            # Department question
            if question.option_source == 'department':
                department = departments.filter(id=value).first()

                if department:
                    answers.append(Answer(submission=submission, question=question, department=department))

            # Normal option
            else:
                option = question.options.filter(id=value, is_active=True).first()

                if option:
                    answers.append( Answer(submission=submission, question=question, selected_option=option))


        # MULTIPLE CHOICE
        elif question.question_type == 'multiple':
            values = request.POST.getlist(field_name)

            if not values:
                continue

            options = question.options.filter(id__in=values, is_active=True)
            for option in options:
                answers.append(Answer(submission=submission, question=question, selected_option=option))

    Answer.objects.bulk_create(answers)

    return submission