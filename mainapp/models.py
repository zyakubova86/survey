import uuid
from django.db import models


class Department(models.Model):
    name_ru = models.CharField(max_length=200, null=True, blank=True, verbose_name='Отдел ru')
    name_uz = models.CharField(max_length=200, null=True, blank=True, verbose_name='Отдел uz')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name_uz


class Question(models.Model):
    TEXT = 'text'
    SINGLE = 'single'
    MULTIPLE = 'multiple'
    NUMBER = 'number'

    QUESTION_TYPES = (
        (TEXT, 'Text'),
        (SINGLE, 'Single Choice'),
        (MULTIPLE, 'Multiple Choice'),
        (NUMBER, 'Number'),
    )

    OPTION_SOURCE_CHOICES = (
        ('manual', 'Manual'),
        ('department', 'Department'),
    )

    question_uz = models.TextField(max_length=200, null=True, blank=True, verbose_name='Вопрос uz')
    question_ru = models.TextField(max_length=200,  null=True, blank=True, verbose_name='Вопрос ru')

    option_source = models.CharField(max_length=50, choices=OPTION_SOURCE_CHOICES, default='manual')
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES, null=True, blank=True, verbose_name='Выбрать тип')
    order = models.PositiveIntegerField(default=0, verbose_name='Номер')

    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Создан')

    is_required = models.BooleanField(default=True, null=True, blank=True, verbose_name='Обязательный')


    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.order}'


class OptionGroup(models.Model):

    name_uz = models.CharField(max_length=255, blank=True)
    name_ru = models.CharField(max_length=255, blank=True)

    order = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Группа варианта"
        verbose_name_plural = "Группы вариантов"

    def __str__(self):
        return self.name_uz

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')

    group = models.ForeignKey(OptionGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='options')

    text_uz = models.CharField(max_length=255, null=True, blank=True, verbose_name='Текст uz')
    text_ru = models.CharField(max_length=255, null=True, blank=True, verbose_name='Текст ru')

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    def __str__(self):
        return self.text_uz

    class Meta:
        ordering = ['question', 'group__order', 'order']
        verbose_name = "Вариант"
        verbose_name_plural = 'Варианты'


class SurveySubmission(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uuid)


class Answer(models.Model):
    submission = models.ForeignKey(SurveySubmission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuestionOption, on_delete=models.SET_NULL, null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = 'Ответы'

        indexes = [
            models.Index(fields=['question']),
            models.Index(fields=['selected_option']),
            models.Index(fields=['created_at']),
        ]