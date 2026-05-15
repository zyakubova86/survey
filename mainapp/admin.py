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
    list_display = ('order', 'question_uz', 'question_ru', 'is_active', 'created_at')
    list_display_links = ('question_uz',)
    filter_horizontal = ('allowed_categories',)

class OptionGroupAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru', 'order')

class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'text_uz', 'group')


class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'created_at')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('submission', 'question','department', 'menu_item', 'selected_option', 'text_answer', 'created_at')


class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru', 'order')


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'name_uz', 'name_ru', 'order', 'is_active')


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(OptionGroup, OptionGroupAdmin)
admin.site.register(QuestionOption, QuestionOptionAdmin)
admin.site.register(SurveySubmission, SurveySubmissionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
