from django.urls import path
from mainapp.views import *

urlpatterns = [
    path('', home, name='home_uz'),
    path('ru/', home, name='home_ru'),

    # path('survey/', submit_survey, name='survey_uz'),
    # path('ru/survey/', submit_survey, name='survey_ru'),

    path('survey/<int:survey_id>', submit_survey, name='survey_uz'),
    path('ru/survey/<int:survey_id>', submit_survey, name='survey_ru'),

    path('thank-you/', thank_you, name='thank_you_uz'),
    path('ru/thank-you/', thank_you, name='thank_you_ru'),

    path('survey/product/<int:survey_id>/', submit_product_survey, name='submit_product_survey_uz'),
    path('ru/survey/product/<int:survey_id>/', submit_product_survey, name='submit_product_survey_ru'),

    path('answers/', dash_answers, name='dash_answers'),
    path('dashboard/', dashboard, name='dashboard'),

]
