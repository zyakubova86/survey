import mimetypes
import os
import uuid
from datetime import timedelta
from pprint import pprint

import pandas as pd
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db.models import Count, ExpressionWrapper, IntegerField, F, FloatField
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from .models import *


def home(request):
    if "/ru/" in request.path:
        template = 'mainapp/home_ru.html'
    else:
        template = 'mainapp/home_uz.html'

    return render(request, template)


def get_departments(request):
    departments = Department.objects.all().order_by('name').filter(is_active=True)

    context = {
        'departments': departments,
    }

    if "/ru/" in request.path:
        template = 'mainapp/departments_ru.html'
    else:
        template = 'mainapp/departments_uz.html'

    return render(request, template, context)


def vote(request, department_name):
    questions = Questions.objects.filter(is_active=True).order_by('id')
    department = get_object_or_404(Department, name=department_name)

    total_questions = Questions.objects.filter(is_active=True).count()

    if request.method == 'POST':
        survey_id = request.session.get('survey_id')
        if not survey_id:
            survey_id = str(uuid.uuid4())
            request.session['survey_id'] = survey_id

        for question in questions:

            selected_option = request.POST.get(f'response_{question.id}')

            option_value = None

            if question.has_options:
                if "/ru/" in request.path:
                    if selected_option == 'option1':
                        question.option1_count += 1
                        option_value = question.option1_ru

                    elif selected_option == 'option2':
                        question.option2_count += 1
                        option_value = question.option2_ru
                    elif selected_option == 'option3':
                        question.option3_count += 1
                        option_value = question.option3_ru
                    elif selected_option == 'option4':
                        question.option4_count += 1
                        option_value = question.option4_ru
                    elif selected_option == 'option5':
                        question.option5_count += 1
                        option_value = question.option5_ru
                else:
                    if selected_option == 'option1':
                        question.option1_count += 1
                        option_value = question.option1_uz
                    elif selected_option == 'option2':
                        question.option2_count += 1
                        option_value = question.option2_uz
                    elif selected_option == 'option3':
                        question.option3_count += 1
                        option_value = question.option3_uz
                    elif selected_option == 'option4':
                        question.option4_count += 1
                        option_value = question.option4_uz
                    elif selected_option == 'option5':
                        question.option5_count += 1
                        option_value = question.option5_uz
                option = selected_option
            else:
                option = 'text'
                option_value = selected_option

            question.save()

            if "/ru/" in request.path:
                question_text = question.question_ru
            else:
                question_text = question.question_uz

            new_employee_response = EmployeeResponse(question=question, question_text=question_text,
                                                     response=option_value, response_option=option,
                                                     department=department, survey_id=survey_id)
            new_employee_response.save()

        SurveyCompletion.objects.get_or_create(
            survey_id=survey_id,
            department=department,
        )

        # reset the session
        request.session['survey_id'] = None

        if "/ru/" in request.path:
            return redirect('thank_you_ru')
        else:
            return redirect('thank_you_uz')

    context = {
        'questions': questions,
        'department': department,
        'total_questions': total_questions,
    }

    if "/ru/" in request.path:
        template = 'mainapp/vote_ru.html'
    else:
        template = 'mainapp/vote_uz.html'

    return render(request, template, context)


def report(request):
    departments = Department.objects.all()
    report_data = []

    for department in departments:
        questions = Questions.objects.all().order_by('pk')
        department_data = {
            'department': department.name,
            'questions': []
        }

        for question in questions:
            responses = EmployeeResponse.objects.filter(department=department, question=question)
            options = []
            total_count = 0

            if question.has_options:
                option1_count = responses.filter(response__in=[question.option1_ru, question.option1_uz]).count()
                option2_count = responses.filter(response__in=[question.option2_ru, question.option2_uz]).count()
                option3_count = responses.filter(response__in=[question.option3_ru, question.option3_uz]).count()
                option4_count = responses.filter(response__in=[question.option4_ru, question.option4_uz]).count()
                option5_count = responses.filter(response__in=[question.option5_ru, question.option5_uz]).count()

                if question.option1_ru or question.option1_uz:
                    options.append({'value': question.option1_ru or question.option1_uz, 'count': option1_count})
                    total_count += option1_count

                if question.option2_ru or question.option2_uz:
                    options.append({'value': question.option2_ru or question.option2_uz, 'count': option2_count})
                    total_count += option2_count

                if question.option3_ru or question.option3_uz:
                    options.append({'value': question.option3_ru or question.option3_uz, 'count': option3_count})
                    total_count += option3_count

                if question.option4_ru or question.option4_uz:
                    options.append({'value': question.option4_ru or question.option4_uz, 'count': option4_count})
                    total_count += option4_count

                if question.option5_ru or question.option5_uz:
                    options.append({'value': question.option5_ru or question.option5_uz, 'count': option5_count})
                    total_count += option5_count

                question_data = {
                    'question_id': question.id,
                    'question_text': question.question_ru,
                    'has_options': True,
                    'options': options,
                    'total_count': total_count
                }
            else:
                response_texts = responses.values_list('response', flat=True)
                question_data = {
                    'question_id': question.id,
                    'question_text': question.question_ru,
                    'has_options': False,
                    'responses': {
                        'response_values': list(response_texts),
                        'response_count': len(response_texts)
                    },
                    'total_count': len(response_texts)
                }

            department_data['questions'].append(question_data)

        if department_data['questions']:
            department_data['questions'].sort(key=lambda x: x['question_id'])
            report_data.append(department_data)

        pprint(report_data)

    context = {
        'report_data': report_data
    }
    return render(request, 'mainapp/report.html', context)


@login_required(login_url='admin_auth')
def report2(request):
    departments = Department.objects.all()
    report_data = []

    for department in departments:
        questions = Questions.objects.all().order_by('pk')
        department_data = {
            'department': department.name,
            'questions': []
        }

        for question in questions:
            responses = EmployeeResponse.objects.filter(department=department, question=question)
            options = []
            total_count = 0

            if question.has_options:
                option1_count, option2_count, option3_count, option4_count, option5_count = 0, 0, 0, 0, 0

                if question.option1_ru or question.option1_uz:
                    option1_count = responses.filter(response=question.option1_ru).count() + responses.filter(
                        response=question.option1_uz).count()
                    options.append({'value': question.option1_ru or question.option1_uz, 'count': option1_count})
                    total_count += option1_count

                if question.option2_ru or question.option2_uz:
                    option2_count = responses.filter(response=question.option2_ru).count() + responses.filter(
                        response=question.option2_uz).count()
                    options.append({'value': question.option2_ru or question.option2_uz, 'count': option2_count})
                    total_count += option2_count

                if question.option3_ru or question.option3_uz:
                    option3_count = responses.filter(response=question.option3_ru).count() + responses.filter(
                        response=question.option3_uz).count()
                    options.append({'value': question.option3_ru or question.option3_uz, 'count': option3_count})
                    total_count += option3_count

                # if question.option4_ru or question.option4_uz:
                #     option4_count = responses.filter(response=question.option4_ru).count() + responses.filter(response=question.option4_uz).count()
                #     options.append({'value': question.option4_ru or question.option4_uz, 'count': option4_count})
                #     total_count += option4_count
                #
                # if question.option5_ru or question.option5_uz:
                #     option5_count = responses.filter(response=question.option5_ru).count() + responses.filter(response=question.option5_uz).count()
                #     options.append({'value': question.option5_ru or question.option5_uz, 'count': option5_count})
                #     total_count += option5_count

                if question.option4_ru:
                    option4_count = responses.filter(response=question.option4_ru).count()
                    options.append({'value': question.option4_ru, 'count': option4_count})
                    total_count += option4_count

                if question.option5_ru:
                    option5_count = responses.filter(response=question.option5_ru).count()
                    options.append({'value': question.option5_ru, 'count': option5_count})
                    total_count += option5_count

                question_data = {
                    'question_id': question.id,
                    'question_text': question.question_ru,
                    'has_options': True,
                    'options': options,
                    'total_count': total_count
                }
            else:
                response_texts = responses.values_list('response', flat=True)
                question_data = {
                    'question_id': question.id,
                    'question_text': question.question_ru,
                    'has_options': False,
                    'responses': {
                        'response_values': list(response_texts),
                        'response_count': len(response_texts)
                    },
                    'total_count': len(response_texts)
                }

            department_data['questions'].append(question_data)

        if department_data['questions']:
            pprint(department_data)
            report_data.append(department_data)

    context = {
        'report_data': report_data
    }

    return render(request, 'mainapp/apanel/report2.html', context)


@login_required(login_url='admin_auth')
def statistics_by_department(request):
    responses = EmployeeResponse.objects.select_related('question', 'department')

    report_data = {}
    for response in responses:
        department_name = response.department.name

        if department_name not in report_data:
            report_data[department_name] = {}

        question_id = response.question
        question_text = response.question.question_ru

        if question_id not in report_data[department_name]:
            report_data[department_name][question_id] = {
                'question_text': question_text,
                'options': {},
                'responses': {
                    'answers': [],
                    'count': 0
                },

            }

        if response.question.has_options:
            if response.response in report_data[department_name][question_id]['options']:
                report_data[department_name][question_id]['options'][response.response] += 1
            else:
                report_data[department_name][question_id]['options'][response.response] = 1
        else:
            report_data[department_name][question_id]['responses']['answers'].append(response.response)
            report_data[department_name][question_id]['responses']['count'] += 1

    # pprint(report_data)

    return render(request, 'mainapp/apanel/statistics_by_department.html', {'report_data': report_data})


def survey(request, department_name, question_id):
    question = get_object_or_404(Questions, id=question_id)
    all_questions = list(Questions.objects.filter(is_active=True).order_by('id'))

    total_questions = Questions.objects.filter(is_active=True).count()
    department = get_object_or_404(Department, name=department_name)

    question_index = all_questions.index(question)
    current_question = question_index + 1
    previous_question_id = all_questions[question_index - 1].id if question_index > 0 else None
    next_question_id = all_questions[question_index + 1].id if question_index < total_questions - 1 else None
    is_last_question = (question_index == len(all_questions) - 1)

    if request.method == 'POST':
        department_name = request.POST['department_name']
        question = Questions.objects.get(id=request.POST['question_id'])

        selected_option = request.POST.get('response')

        if question.has_options:
            if selected_option == 'option1_uz' or selected_option == 'option1_ru':
                question.option1_count += 1
            if selected_option == 'option2_uz' or selected_option == 'option2_ru':
                question.option2_count += 1
            if selected_option == 'option3_uz' or selected_option == 'option3_ru':
                question.option3_count += 1
            if selected_option == 'option4_uz' or selected_option == 'option4_ru':
                question.option4_count += 1
            if selected_option == 'option5_uz' or selected_option == 'option5_ru':
                question.option5_count += 1

        new_employee_response = EmployeeResponse(question=question, response=selected_option, department=department)
        new_employee_response.save()

        next_question_id = request.POST.get('next_question_id')

        if next_question_id != 'None':
            if "/ru/" in request.path:
                return redirect('survey_ru', department_name=department_name, question_id=next_question_id)
            else:
                return redirect('survey_uz', department_name=department_name, question_id=next_question_id)
        else:
            if "/ru/" in request.path:
                return redirect('thank_you_ru')
            else:
                return redirect('thank_you_uz')

    context = {
        'question': question,
        'department_name': department,
        'total_questions': total_questions,
        'current_question': current_question,
        'previous_question_id': previous_question_id,
        'next_question_id': next_question_id,
        'is_last_question': is_last_question,
    }

    if "/ru/" in request.path:
        template = 'mainapp/survey_ru.html'
    else:
        template = 'mainapp/survey_uz.html'

    return render(request, template, context)


def thank_you(request):
    if "/ru/" in request.path:
        template = 'mainapp/thank_you_ru.html'
    else:
        template = 'mainapp/thank_you_uz.html'
    return render(request, template)


@login_required(login_url='admin_auth')
def a_panel(request):
    if request.user.is_authenticated:
        template = 'mainapp/apanel/apanel.html'

        employee_responses = EmployeeResponse.objects.all().order_by('-pk')

        context = {'employee_responses': employee_responses}

        return render(request, template, context)
    else:
        return redirect('admin_auth')


@login_required(login_url='admin_auth')
def report_all(request):
    departments = Department.objects.all()
    report_data = []

    for department in departments:
        questions = Questions.objects.all()
        department_data = {
            'department': department.name,
            'questions': []
        }

        for question in questions:
            responses = EmployeeResponse.objects.filter(department=department, question=question)

            if question.has_options:
                options = []
                if question.option1:
                    options.append(
                        {'value': question.option1, 'count': responses.filter(response=question.option1).count()})
                if question.option2:
                    options.append(
                        {'value': question.option2, 'count': responses.filter(response=question.option2).count()})
                if question.option3:
                    options.append(
                        {'value': question.option3, 'count': responses.filter(response=question.option3).count()})
                if question.option4:
                    options.append(
                        {'value': question.option4, 'count': responses.filter(response=question.option4).count()})
                if question.option5:
                    options.append(
                        {'value': question.option5, 'count': responses.filter(response=question.option5).count()})

                question_data = {
                    'question_text': question.question_text,
                    'has_options': True,
                    'options': options
                }
            else:
                response_texts = responses.values_list('response', flat=True)
                question_data = {
                    'question_text': question.question_text,
                    'has_options': False,
                    'responses': {
                        'response_values': list(response_texts),
                        'response_count': len(response_texts)
                    }
                }

            department_data['questions'].append(question_data)

        report_data.append(department_data)

    context = {
        'report_data': report_data
    }

    return render(request, 'mainapp/apanel/report_all.html', context)


@login_required(login_url='admin_auth')
def report_by_department(request):
    responses = EmployeeResponse.objects.select_related('question', 'department')
    report_data = {}

    for response in responses:
        department_name = response.department.name
        if department_name not in report_data:
            report_data[department_name] = {}

        question_text = response.question.question_text_ru
        if question_text not in report_data[department_name]:
            report_data[department_name][question_text] = {
                'options': {},
                'responses': {
                    'answers': [],
                    'count': 0
                },

            }

        if response.question.has_options:
            if response.response in report_data[department_name][question_text]['options']:
                report_data[department_name][question_text]['options'][response.response] += 1
            else:
                report_data[department_name][question_text]['options'][response.response] = 1
        else:
            report_data[department_name][question_text]['responses']['answers'].append(response.response)
            report_data[department_name][question_text]['responses']['count'] += 1

    return render(request, 'mainapp/apanel/report_by_department.html', {'report_data': report_data})


@login_required(login_url='admin_auth')
def upload_file(request):
    template = 'mainapp/apanel/upload_file.html'

    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']

        if not os.path.exists('mainapp/media/'):
            os.makedirs('mainapp/media/')

        # Delete existing file if exists
        if os.path.exists('mainapp/media/'):
            existing_files = os.listdir('mainapp/media/')
            for file in existing_files:
                os.remove(f'mainapp/media/{file}')

        # Check if the uploaded file is an Excel file
        if mimetypes.guess_type(excel_file.name)[0] not in ['application/vnd.ms-excel',
                                                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
            return render(request, template, {'upload_message': 'Файл должен быть формата xlsx или xls'})

        # Save uploaded file
        fs = FileSystemStorage(location=f'mainapp/media/')
        filename = fs.save(excel_file.name, excel_file)
        uploaded_file_url = fs.url(filename)

        # Save data to the database
        Employees.objects.all().delete()
        Department.objects.all().delete()

        df = pd.read_excel(f'mainapp/media/{filename}')

        # for i, row in df.iterrows():
        #     employees = Employees(code=row['Код'], name=row['ФИО'], department=row['Отдел'])
        #     employees.save()

        departments = df['Отдел'].dropna().unique()
        for department in departments:
            if '.' in department:
                department = department.replace('.', '')

            new_department = Department(name=department)
            new_department.save()

        context = {
            'uploaded_file_url': uploaded_file_url,
            'excel_file': excel_file,
            'upload_message': "Data saved successfully"
        }
        return render(request, template, context)
    else:
        return render(request, template)


@login_required(login_url='admin_auth')
def upload_questions(request):
    template = 'mainapp/apanel/upload_questions.html'
    if request.method == "POST":
        questions_file = request.FILES['questions_file']

        if mimetypes.guess_type(questions_file.name)[0] not in ['application/vnd.ms-excel',
                                                                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
            return render(request, template, {'upload_message': 'Файл должен быть формата xlsx или xls'})

        # Save uploaded file
        if not os.path.exists('mainapp/media/'):
            os.makedirs('mainapp/media/')

        # Delete existing file if exists
        if os.path.exists('mainapp/media/'):
            existing_files = os.listdir('mainapp/media/')
            for file in existing_files:
                os.remove(f'mainapp/media/{file}')

        fs = FileSystemStorage(location=f'mainapp/media/')
        filename = fs.save(questions_file.name, questions_file)
        uploaded_file_url = fs.url(filename)

        try:
            # Save data to the database
            df = pd.read_excel(f'mainapp/media/{filename}')

            # question has many options
            for i, row in df.iterrows():
                question_text = row['Вопрос']
                if pd.isnull(question_text):
                    raise ValidationError('Пустое значение в столбце "Вопрос"')

                has_options = row['Есть варианты']

                if pd.isnull(has_options):
                    raise ValidationError('Пустое значение в столбце "Есть варианты"')
                option1 = None
                option2 = None
                option3 = None
                option4 = None
                option5 = None

                if has_options:
                    if pd.isnull(row['Вариант1']):
                        option1 = None
                    else:
                        option1 = row['Вариант1']

                    if pd.isnull(row['Вариант2']):
                        option2 = None
                    else:
                        option2 = row['Вариант2']

                    if pd.isnull(row['Вариант3']):
                        option3 = None
                    else:
                        option3 = row['Вариант3']

                    if pd.isnull(row['Вариант4']):
                        option4 = None
                    else:
                        option4 = row['Вариант4']

                    if pd.isnull(row['Вариант5']):
                        option5 = None
                    else:
                        option5 = row['Вариант5']

                question = Questions(question_text=question_text, has_options=has_options, option1=option1,
                                     option2=option2, option3=option3, option4=option4, option5=option5)
                question.save()

            context = {
                'questions_file': questions_file,
                'uploaded_file_url': uploaded_file_url,
                'upload_message': "Вопросы успешно загружены"
            }
            return render(request, template, context)

        except Exception as e:
            return render(request, template, {'upload_message': e})

    return render(request, template)


@login_required(login_url='admin_auth')
def questions_list(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        question_text = request.POST.get('question_text')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        option5 = request.POST.get('option5')
        has_options = 'has_options' in request.POST

        question = get_object_or_404(Questions, id=question_id)
        question.question_text = question_text
        question.option1 = option1
        question.option2 = option2
        question.option3 = option3
        question.option4 = option4
        question.option5 = option5
        question.has_options = has_options
        question.save()
        return redirect('questions_list')

    questions = Questions.objects.all().order_by('id')

    context = {
        'questions': questions
    }
    return render(request, 'mainapp/apanel/questions_list.html', context)


@login_required(login_url='admin_auth')
def question_create(request):
    if request.method == "POST":
        question = Questions()
        question.question_ru = request.POST.get('question_ru')
        question.question_uz = request.POST.get('question_uz')

        question.is_active = 'is_active' in request.POST
        question.has_options = 'has_options' in request.POST

        question.option1_ru = request.POST.get('option1_ru', '')
        question.option1_uz = request.POST.get('option1_uz', '')
        question.option2_ru = request.POST.get('option2_ru', '')
        question.option2_uz = request.POST.get('option2_uz', '')
        question.option3_ru = request.POST.get('option3_ru', '')
        question.option3_uz = request.POST.get('option3_uz', '')
        question.option4_ru = request.POST.get('option4_ru', '')
        question.option4_uz = request.POST.get('option4_uz', '')
        question.option5_ru = request.POST.get('option5_ru', '')
        question.option5_uz = request.POST.get('option5_uz', '')
        question.save()

        return redirect('questions_list')

    return render(request, 'mainapp/apanel/question_create.html')


@login_required(login_url='admin_auth')
def question_update(request, pk):
    question = get_object_or_404(Questions, id=pk)

    if request.method == "POST":
        question.question_ru = request.POST.get('question_ru')
        question.question_uz = request.POST.get('question_uz')
        question.is_active = 'is_active' in request.POST
        question.has_options = 'has_options' in request.POST
        question.option1_ru = request.POST.get('option1_ru')
        question.option1_uz = request.POST.get('option1_uz')
        question.option2_ru = request.POST.get('option2_ru')
        question.option2_uz = request.POST.get('option2_uz')
        question.option3_ru = request.POST.get('option3_ru')
        question.option3_uz = request.POST.get('option3_uz')
        question.option4_ru = request.POST.get('option4_ru')
        question.option4_uz = request.POST.get('option4_uz')
        question.option5_ru = request.POST.get('option5_ru')
        question.option5_uz = request.POST.get('option5_uz')
        question.save()
        return redirect('questions_list')

    context = {
        'question': question,
    }
    return render(request, 'mainapp/apanel/question_update.html', context)


@login_required(login_url='admin_auth')
def question_delete(request, pk):
    template = 'mainapp/apanel/question_delete.html'

    question = get_object_or_404(Questions, id=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('questions_list')

    context = {
        'question': question,
    }
    return render(request, template, context)


def admin_auth(request):
    if request.method == 'GET':
        template = 'mainapp/apanel/admin_auth.html'
        return render(request, template)
    elif request.method == "POST":
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            return redirect('admin_auth')
        else:
            login(request, user)
            return redirect('apanel')


@login_required(login_url='admin_auth')
def departments_list(request):
    departments = Department.objects.all().order_by('name')

    context = {
        'departments': departments
    }
    return render(request, 'mainapp/apanel/departments_list.html', context)


@login_required(login_url='admin_auth')
def department_create(request):
    template = 'mainapp/apanel/department_create.html'
    if request.method == "POST":
        department = Department()
        department.name = request.POST['department_name_ru']
        department.name_uz = request.POST['department_name_uz']
        department.is_active = 'is_active' in request.POST
        department.save()

        return redirect('departments_list')

    return render(request, template)


@login_required(login_url='admin_auth')
def department_update(request, pk):
    template = 'mainapp/apanel/department_update.html'
    department = get_object_or_404(Department, id=pk)

    if request.method == "POST":
        department = Department.objects.get(pk=request.POST['department_id'])
        department.name = request.POST['department_name_ru']
        department.name_uz = request.POST['department_name_uz']
        department.is_active = 'is_active' in request.POST
        department.save()

        return redirect('departments_list')

    context = {
        'department': department,
    }

    return render(request, template, context)


@login_required(login_url='admin_auth')
def department_delete(request, pk):
    template = 'mainapp/apanel/department_delete.html'
    department = get_object_or_404(Department, id=pk)

    if request.method == "POST":
        department.delete()
        return redirect('departments_list')

    context = {
        'department': department,
    }
    return render(request, template, context)


@login_required(login_url='admin_auth')
def get_suggestions(request):
    text_responses = EmployeeResponse.objects.filter(response_option='text').order_by('-created_at')

    context = {
        'text_responses': text_responses
    }
    return render(request, 'mainapp/apanel/suggestions.html', context)


@login_required(login_url='admin_auth')
def statistics_by_date(request):
    template = 'mainapp/apanel/statistics_by_date.html'
    questions_count = Questions.objects.all().filter(is_active=True).count()

    total_responses_today = 0
    total_responses_this_week = 0
    total_responses_this_month = 0
    total_responses_yesterday = 0

    today = now().date()
    yesterday = today - timedelta(days=1)
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # Query to get responses for today
    responses_today = EmployeeResponse.objects.filter(
        created_at__date=today
    ).values('department__name').annotate(count=Count('id'))

    # Divide responses for today by count of active questions
    responses_today = responses_today.annotate(
        count_per_question=ExpressionWrapper(
            F('count') / questions_count, output_field=IntegerField()
        )
    )
    for res in responses_today:
        total_responses_today += res['count_per_question']

    # Query to get responses for yesterday
    responses_yesterday = EmployeeResponse.objects.filter(
        created_at__date=yesterday
    ).values('department__name').annotate(count=Count('id'))

    # Divide responses for yesterday by count of active questions
    responses_yesterday = responses_yesterday.annotate(
        count_per_question=ExpressionWrapper(
            F('count') / questions_count, output_field=IntegerField()
        )
    )
    for res in responses_yesterday:
        total_responses_yesterday += res['count_per_question']

    responses_this_week = EmployeeResponse.objects.filter(
        created_at__date__gte=start_of_week
    ).values('department__name').annotate(
        count=Count('id'),
        count_per_question=ExpressionWrapper(
            Count('id') / questions_count,
            output_field=FloatField()
        )
    )

    for res in responses_this_week:
        total_responses_this_week += res['count_per_question']

    responses_this_month = EmployeeResponse.objects.filter(
        created_at__date__gte=start_of_month
    ).values('department__name').annotate(
        count=Count('id'),
        count_per_question=ExpressionWrapper(
            Count('id') / questions_count,
            output_field=FloatField()
        )
    )

    for res in responses_this_month:
        total_responses_this_month += res['count_per_question']

    context = {
        'responses_today': responses_today,
        'responses_yesterday': responses_yesterday,
        'responses_this_week': responses_this_week,
        'responses_this_month': responses_this_month,
        'questions_count': questions_count,
        'total_responses_today': int(total_responses_today),
        'total_responses_this_week': int(total_responses_this_week),
        'total_responses_this_month': int(total_responses_this_month),
        'total_responses_yesterday': int(total_responses_yesterday),

    }

    return render(request, template, context)


@login_required(login_url='admin_auth')
def get_response_count_by_date(request):
    template = 'mainapp/apanel/response_count_by_date.html'

    # today = now().date()
    # week = today - timedelta(days=today.weekday())
    # month = today.replace(day=1)

    count_per_date_department = (SurveyCompletion.objects.values('completed_at__date', 'department__name')
                                 .annotate(count=Count('survey_id', distinct=True)).order_by('-completed_at__date',
                                                                                             'department__name'))

    total_count_per_date = (SurveyCompletion.objects.values('completed_at__date')
                            .annotate(total_count=Count('survey_id', distinct=True)).order_by('-completed_at__date'))

    total_count_dict = {item['completed_at__date']: item['total_count'] for item in total_count_per_date}
    response_count_start_datetime = SurveyCompletion.objects.order_by('completed_at').first().completed_at

    context = {
        'count_per_date_department': count_per_date_department,
        'total_count_per_date': total_count_per_date,
        'total_count_dict': total_count_dict,
        'response_count_start_datetime': response_count_start_datetime,
    }

    return render(request, template, context)


@login_required(login_url='admin_auth')
def get_response_count_by_department(request):
    template = 'mainapp/apanel/response_count_by_department.html'
    department_count_per_date = (SurveyCompletion.objects.values('completed_at__date', 'department__name')
                                 .annotate(count=Count('survey_id', distinct=True)).order_by('-completed_at__date',
                                                                                             'department__name'))
    response_count_start_datetime = SurveyCompletion.objects.order_by('completed_at').first().completed_at

    context = {
        'department_count_per_date': department_count_per_date,
        'response_count_start_datetime': response_count_start_datetime,
    }

    return render(request, template, context)