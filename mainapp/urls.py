from django.urls import path
from mainapp.views import *

urlpatterns = [
    path('', home, name='home_uz'),
    path('ru/', home, name='home_ru'),

    path('survey/', submit_survey, name='survey_uz'),
    path('ru/survey/', submit_survey, name='survey_ru'),

]
