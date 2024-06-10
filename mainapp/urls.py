from django.urls import path
from mainapp.views import *

urlpatterns = [
    path('', home, name='home_uz'),
    path('ru/', home, name='home_ru'),

    path('departments/', get_departments, name='departments_uz'),
    path('ru/departments/', get_departments, name='departments_ru'),

    path('department/<str:department_name>/', vote, name='vote_uz'),
    path('ru/department/<str:department_name>/', vote, name='vote_ru'),

    path('thank-you/', thank_you, name='thank_you_uz'),
    path('ru/thank-you/', thank_you, name='thank_you_ru'),

    # Admin panel urls
    path('apanel/', a_panel, name='apanel'),
    path('apanel/auth/', admin_auth, name='admin_auth'),

    path('apanel/upload/', upload_file, name='upload_file'),
    path('apanel/upload-questions/', upload_questions, name='upload_questions'),

    path('apanel/report-all/', report_all, name='report_all'),
    path('apanel/report-department/', report_by_department, name='report_by_department'),
    path('apanel/report-department/', report_by_department, name='report_by_department'),

    path('apanel/departments/', departments_list, name='departments_list'),
    path('apanel/departments/create/', department_create, name='department_create'),
    path('apanel/departments/update/<int:pk>/', department_update, name='department_update'),
    path('apanel/departments/delete/<int:pk>/', department_delete, name='department_delete'),

    path('apanel/questions/', questions_list, name='questions_list'),
    path('apanel/questions/create/', question_create, name='question_create'),
    path('apanel/questions/update/<int:pk>/', question_update, name='question_edit'),
    path('apanel/questions/delete/<int:pk>/', question_delete, name='question_delete'),

    path('apanel/statistics/', statistics_by_department, name='statistics'),
    path('apanel/report2/', report2, name='report2'),

]
