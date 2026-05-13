from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render, redirect

from .models import *


def home(request):
    if "/ru/" in request.path:
        template = 'mainapp/home_ru.html'
    else:
        template = 'mainapp/home_uz.html'

    return render(request, template)


def get_lang(request):
    return "ru" if "/ru/" in request.path else "uz"


@transaction.atomic
def submit_survey(request):
    lang = get_lang(request)
    if "/ru/" in request.path:
        template = 'mainapp/survey_ru.html'
        redirect_url = 'thank_you_ru'
    else:
        template = 'mainapp/survey_uz.html'
        redirect_url = 'thank_you_uz'

    questions = Question.objects.filter(is_active=True).prefetch_related('options').order_by('order')
    departments = Department.objects.filter(is_active=True, name_uz__isnull=False, name_ru__isnull=False).exclude(name_uz='', name_ru='').order_by(f'name_{lang}')
    menu_items = MenuItem.objects.filter(is_active=True).select_related('category')

    if request.method == 'POST':
        save_answers(request=request, questions=questions, departments=departments)
        return redirect(redirect_url)

    context = {
        'questions': questions,
        'departments': departments,
        'menu_items': menu_items,
        'lang': lang,
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
                answers.append(Answer(submission=submission, question=question, text_answer=value))


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

            # MENU ITEMS
            if question.option_source == 'menu':

                for value in values:

                    item = MenuItem.objects.filter(
                        id=value,
                        is_active=True
                    ).first()

                    if item:
                        answers.append(Answer(
                            submission=submission,
                            question=question,
                            menu_item=item
                        )
                        )

            # NORMAL OPTIONS
            else:
                options = question.options.filter(id__in=values, is_active=True)
                for option in options:
                    answers.append(Answer(submission=submission, question=question, selected_option=option))

    Answer.objects.bulk_create(answers)

    return submission


@login_required
def answers_list_view(request):
    submissions = SurveySubmission.objects.prefetch_related(
        'answers__question',
        'answers__selected_option',
        'answers__department',
        'answers__menu_item',
    ).order_by('-created_at')

    questions = Question.objects.filter(
        is_active=True
    ).order_by('order')

    rows = []

    for submission in submissions:

        row = {
            'submission': submission,
            'answers': {}
        }

        for answer in submission.answers.all():

            value = ''

            # TEXT ANSWER
            if answer.text_answer:
                value = answer.text_answer

            # NORMAL OPTION
            elif answer.selected_option:
                value = answer.selected_option.text_uz

            # DEPARTMENT
            elif answer.department:
                value = answer.department.name_uz

            # MENU ITEM
            elif answer.menu_item:
                value = answer.menu_item.name_uz

            question_id = answer.question.id

            if question_id not in row['answers']:
                row['answers'][question_id] = []

            row['answers'][question_id].append(value)

        rows.append(row)

    context = {
        'questions': questions,
        'rows': rows,
    }

    return render(
        request,
        'mainapp/answers_list.html',
        context
    )


@login_required
def analytics_view(request):

    # TOTAL SUBMISSIONS BY DATE
    total_by_date = (
        SurveySubmission.objects
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(total=Count('id'))
        .order_by('-date')
    )

    # DEPARTMENT TOTALS
    department_totals = (
        Answer.objects
        .filter(department__isnull=False)
        .values(
            'department__name_uz',
            'department__name_ru'
        )
        .annotate(total=Count('submission', distinct=True))
        .order_by('-total')
    )

    # DEPARTMENT BY DATE
    department_by_date = (
        Answer.objects
        .filter(department__isnull=False)
        .annotate(date=TruncDate('created_at'))
        .values(
            'date',
            'department__name_uz',
            'department__name_ru'
        )
        .annotate(total=Count('submission', distinct=True))
        .order_by('-date')
    )

    context = {
        # 'total_by_date': total_by_date,
        # 'department_totals': department_totals,
        # 'department_by_date': department_by_date,
    }

    return render(request, 'mainapp/analytics.html', context)