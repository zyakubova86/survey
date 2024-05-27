from django.urls import path
from mainapp.views import *

urlpatterns = [
    path('', home, name='home_uz'),
    path('ru/', home, name='home_ru'),

    path('departments/', get_departments, name='departments_uz'),
    path('ru/departments/', get_departments, name='departments_ru'),

    path('department/<str:department_name>/', vote, name='vote_uz'),
    path('ru/department/<str:department_name>/', vote, name='vote_ru'),

    path('report/', report, name='report'),

    # path('statistics/', statistics_by_department, name='statistics'),
    # path('report2/', report2, name='report2'),
    # path('department/<str:department_name>/<int:question_id>/', survey, name='survey_uz'),
    # path('ru/department/<str:department_name>/<int:question_id>/', survey, name='survey_ru'),

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

    path('apanel/questions/', questions_list, name='questions_list'),

    path('apanel/statistics/', statistics_by_department, name='statistics'),
    path('apanel/report2/', report2, name='report2'),

    # path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),

]
