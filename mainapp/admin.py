import pandas as pd
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from .models import *
from io import BytesIO


class DepartmentAdmin(admin.ModelAdmin):
    ordering = ('name_uz', 'name_uz')
    list_display = ('name_uz', 'name_ru')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'question_uz',  'is_active', 'created_at')
    list_display_links = ('question_uz',)

class OptionGroupAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru', 'order')

class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'text_uz', 'group')


class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'created_at')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('submission', 'question','department', 'selected_option', 'text_answer', 'created_at')


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(OptionGroup, OptionGroupAdmin)
admin.site.register(QuestionOption, QuestionOptionAdmin)
admin.site.register(SurveySubmission, SurveySubmissionAdmin)
admin.site.register(Answer, AnswerAdmin)
