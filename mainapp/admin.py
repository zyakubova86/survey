from django.contrib import admin

from .models import *


class DepartmentAdmin(admin.ModelAdmin):
    ordering = ('name_uz', 'name_uz')
    list_display = ('name_uz', 'name_ru')


class SurveyAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = ('id', 'title_uz', 'title_ru', 'survey_type', 'order', 'is_active', 'created_at')
    list_display_links = ('id', 'title_uz', 'title_ru')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'question_uz', 'order', 'is_active')
    list_display_links = ('question_uz',)
    filter_horizontal = ('allowed_categories',)

    ordering = ('survey', 'order',)


class OptionGroupAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru', 'order')


class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'text_uz', 'text_ru')


class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'survey', 'created_at')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('submission', 'question', 'selected_option', 'menu_item', 'department', 'text_answer', 'created_at')


class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru', 'order')


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'name_uz', 'name_ru', 'order', 'is_active')


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(OptionGroup, OptionGroupAdmin)
admin.site.register(QuestionOption, QuestionOptionAdmin)
admin.site.register(SurveySubmission, SurveySubmissionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
