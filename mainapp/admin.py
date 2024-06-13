import pandas as pd
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from .models import *
from io import BytesIO


class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department')
    list_filter = ('name', "department")

    class Meta:
        ordering = ('name',)
        verbose_name = "Сотрудники"
        verbose_name_plural = "Сотрудники"


class DepartmentAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name',)

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'question_ru', 'question_uz',  'is_active', 'has_options', 'option1_ru', 'option1_uz', 'option2_ru', 'option2_uz', 'option3_ru', 'option3_uz', 'option4_ru', 'option5_ru', 'option4_uz', 'option5_uz', 'created', 'option1_count', 'option2_count', 'option3_count', 'option4_count', 'option5_count')
    # list_filter = ('question_ru', 'question_uz',  'is_active', 'has_options', 'option1_ru', 'option1_uz', 'option2_ru', 'option2_uz', 'option3_ru', 'option3_uz', 'option4_ru', 'option5_ru', 'option4_uz', 'option5_uz', 'created', 'option1_count', 'option2_count', 'option3_count', 'option4_count', 'option5_count')


    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = 'Вопросы'


class EmployeeResponseAdmin(admin.ModelAdmin):
    list_display = ('survey_id', 'question', 'question_text', 'response', 'response_option', 'department', 'created_at')
    # list_filter = ('question', 'response', 'department')

    class Meta:
        verbose_name = "Ответ сотрудника"
        verbose_name_plural = 'Ответы сотрудников'


class SurveyCompletionAdmin(admin.ModelAdmin):
    ordering = ('-completed_at',)
    list_display = ('id', 'survey_id', 'department', 'completed_at')

    class Meta:
        verbose_name = "Завершенные опросы"
        verbose_name_plural = 'Завершенные опросы'


admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(EmployeeResponse, EmployeeResponseAdmin)
admin.site.register(SurveyCompletion, SurveyCompletionAdmin)