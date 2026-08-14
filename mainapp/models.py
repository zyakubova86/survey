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
        return str(self.name_uz)


class Survey(models.Model):
    GENERAL = 'general'
    PRODUCT = 'product'

    SURVEY_TYPES = (
        (GENERAL, 'Умумий'),
        (PRODUCT, 'Янги маҳсулот'),
    )

    title_uz = models.CharField(max_length=255, verbose_name="Название_uz")
    title_ru = models.CharField(max_length=255, verbose_name="Название_ru")

    survey_type = models.CharField(max_length=30, choices=SURVEY_TYPES, default=GENERAL, verbose_name="Тип опроса")

    image = models.ImageField(upload_to="surveys/", null=True, blank=True, verbose_name="Картинка")
    description_uz = models.TextField(blank=True, verbose_name="Описание_uz")
    description_ru = models.TextField(blank=True, verbose_name="Описание_ru")
    order = models.PositiveIntegerField(default=0, verbose_name='№ номер')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = 'Опросники'


    def __str__(self):
        return self.title_uz


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
        ('manual', 'Вручную'),
        ('department', 'Отделы'),
        ('menu', 'Меню'),
    )

    question_uz = models.TextField(max_length=200, null=True, blank=True, verbose_name='Вопрос uz')
    question_ru = models.TextField(max_length=200,  null=True, blank=True, verbose_name='Вопрос ru')

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions", verbose_name="Сўровнома", null=True, blank=True)

    order = models.PositiveIntegerField(default=0, verbose_name='№ номер')

    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES, null=True, blank=True, verbose_name='Тип вопроса')
    option_source = models.CharField(max_length=50, choices=OPTION_SOURCE_CHOICES, default='manual', verbose_name='Тип варианта')
    allowed_categories = models.ManyToManyField('FoodCategory', blank=True, related_name='questions', verbose_name='Разрешенные категории')

    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_required = models.BooleanField(default=True, null=True, blank=True, verbose_name='Обязательный')

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Создан')

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
        return str(self.name_uz)

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text_uz = models.CharField(max_length=255, null=True, blank=True, verbose_name='Текст uz')
    text_ru = models.CharField(max_length=255, null=True, blank=True, verbose_name='Текст ru')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    def __str__(self):
        return str(self.text_uz)

    class Meta:
        ordering = ['question', 'order']
        verbose_name = "Вариант"
        verbose_name_plural = 'Варианты'


class SurveySubmission(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT, related_name="submissions", null=True, blank=True, verbose_name="Опрос тип")
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
    menu_item = models.ForeignKey(
        "MenuItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = 'Ответы'

        indexes = [
            models.Index(fields=['question']),
            models.Index(fields=['selected_option']),
            models.Index(fields=['created_at']),
        ]


    def __str__(self):

        if self.text_answer:
            return self.text_answer

        if self.selected_option:
            return str(self.selected_option)

        if self.department:
            return str(self.department)

        return f'Answer #{self.id}'


class FoodCategory(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Категория блюд"
        verbose_name_plural = 'Категории блюд'

    def __str__(self):
        return str(self.name_uz)


class MenuItem(models.Model):
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='items')
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category__order', 'order']

        verbose_name = "Название блюд"
        verbose_name_plural = 'Названия блюд'

    def __str__(self):
        return str(self.name_uz)