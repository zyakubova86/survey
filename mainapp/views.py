import calendar
from collections import defaultdict
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.shortcuts import render, redirect
from django.utils import timezone

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

    # questions = Question.objects.filter(is_active=True).prefetch_related('options').order_by('order')
    questions = Question.objects.filter(is_active=True).prefetch_related('options',
                                                                         'allowed_categories__items').order_by('order')
    departments = Department.objects.filter(is_active=True, name_uz__isnull=False, name_ru__isnull=False).exclude(
        name_uz='', name_ru='').order_by(f'name_{lang}')
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
                    answers.append(Answer(submission=submission, question=question, selected_option=option))


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
def dashboard(request):
    now = timezone.localtime(timezone.now())

    total_submissions = SurveySubmission.objects.count()
    today_total = SurveySubmission.objects.filter(created_at__date=now.date()).count()
    week_total = SurveySubmission.objects.filter(created_at__gte=now - timedelta(days=7)).count()
    month_total = SurveySubmission.objects.filter(created_at__month=now.month, created_at__year=now.year).count()

    # DAILY STATS (CURRENT MONTH DAYS)
    daily_queryset = (SurveySubmission.objects.annotate(day=TruncDate("created_at")).values("day").annotate(
        total=Count("id")).order_by("day"))
    daily_map = {
        item["day"]: item["total"]
        for item in daily_queryset
    }

    daily_stats = []
    for day_num in range(1, now.day + 1):
        current_day = date(now.year, now.month, day_num)

        daily_stats.append({
            "day": current_day.strftime("%d"),
            "total": daily_map.get(current_day, 0)
        })

    # WEEKLY STATS (CURRENT MONTH WEEKS)
    start_month = date(now.year, now.month, 1)
    end_date = now.date()
    start_weekday = start_month.weekday()
    print("start_weekday", start_weekday)

    # create week index manually
    weekly_map = defaultdict(int)

    # get all submissions for current month
    qs = SurveySubmission.objects.filter(
        created_at__date__gte=start_month,
        created_at__date__lte=end_date
    )

    for obj in qs:
        d = obj.created_at.date()
        # position in month grid
        day_index = d.day + start_weekday - 1
        week_index = (day_index // 7) + 1
        weekly_map[week_index] += 1

    days_in_month = calendar.monthrange(now.year, now.month)[1]
    total_weeks = ((days_in_month + start_weekday - 1) // 7) + 1

    print("days_in_month", days_in_month)
    print("weekly_map", weekly_map)
    print("total_weeks", total_weeks)

    weekly_stats = []

    for w in range(1, total_weeks + 1):
        weekly_stats.append({
            "week": f"{w}",
            "total": weekly_map.get(w, 0)
        })

    # MONTHLY STATS (CURRENT YEAR MONTHS)
    monthly_queryset = (SurveySubmission.objects.annotate(month=TruncMonth("created_at")).values("month").annotate(
        total=Count("id")).order_by("month"))
    monthly_map = {
        item["month"].month: item["total"]
        for item in monthly_queryset
    }
    RU_MONTHS = {
        1: "янв",
        2: "фев",
        3: "мар",
        4: "апр",
        5: "май",
        6: "июнь",
        7: "июль",
        8: "авг",
        9: "сент",
        10: "окт",
        11: "ноя",
        12: "дек",
    }
    monthly_stats = []

    for month_num in range(1, now.month + 1):
        current_month = date(now.year, month_num, 1)

        monthly_stats.append({
            # "month": str(current_month.strftime("%m")), current_month.strftime("%Y-%m")
            # "month": str(current_month.month),
            "month": RU_MONTHS[current_month.month],
            "total": monthly_map.get(month_num, 0)
        })

    # DEPARTMENT STATS
    department_stats = (Answer.objects.filter(department__isnull=False).values("department__name_uz").annotate(
        total=Count("submission", distinct=True)).order_by("-total"))

    department_kpis = (Answer.objects.filter(department__isnull=False).values("department__name_uz").annotate(

        today=Count(
            "submission",
            filter=Q(created_at__date=now.date()),
            distinct=True
        ),

        week=Count(
            "submission",
            filter=Q(created_at__gte=now - timedelta(days=7)),
            distinct=True
        ),

        month=Count(
            "submission",
            filter=Q(
                created_at__month=now.month,
                created_at__year=now.year
            ),
            distinct=True
        ),

        total=Count(
            "submission",
            distinct=True
        )

    )
                       .order_by("-month")
                       )

    recent_answers = (
        Answer.objects.select_related('question', 'selected_option', 'department', 'menu_item').order_by('-created_at'))

    context = {
        'today_total': today_total,
        'week_total': week_total,
        'month_total': month_total,
        'total_submissions': total_submissions,

        "daily_stats": daily_stats,
        "weekly_stats": weekly_stats,
        "monthly_stats": monthly_stats,

        "department_stats": list(department_stats),
        'department_kpis': list(department_kpis),

        "recent_answers": list(recent_answers),
    }

    return render(request, 'mainapp/dashboard.html', context)


@login_required
def dash_answers(request):
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
        'mainapp/dash_answers.html',
        context
    )
