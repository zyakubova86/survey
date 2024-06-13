from django.db import models


class Employees(models.Model):
    code = models.IntegerField(null=True, verbose_name='Код')
    name = models.CharField(max_length=200, null=True, verbose_name='Имя')
    department = models.CharField(max_length=200, null=True, verbose_name='Отдел')

    class Meta:
        verbose_name = "Сотрудники"
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Отдел ru')
    name_uz = models.CharField(max_length=200, null=True, blank=True, verbose_name='Отдел uz')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name


class Questions(models.Model):
    question_ru = models.TextField(max_length=200, null=True, blank=True, verbose_name='Вопрос ru')
    question_uz = models.TextField(max_length=200, null=True, blank=True, verbose_name='Вопрос uz')

    is_active = models.BooleanField(default=True, verbose_name='Активен')
    has_options = models.BooleanField(default=False, verbose_name='Есть варианты')

    option1_ru = models.CharField(max_length=30, null=True, blank=True, verbose_name='Вариант_1_ru')
    option1_uz = models.CharField(max_length=30, null=True, blank=True, verbose_name='Вариант_1_uz')

    option2_ru = models.CharField(max_length=30, null=True, blank=True, verbose_name='Вариант_2_ru')
    option2_uz = models.CharField(max_length=30, null=True, blank=True, verbose_name='Вариант_2_uz')

    option3_ru = models.CharField(max_length=30, null=True, blank=True, verbose_name='Вариант_3_ru')
    option3_uz = models.CharField(max_length=30, null=True, blank=True, verbose_name='Вариант_3_uz')

    option4_ru = models.CharField(max_length=30, null=True, blank=True, verbose_name='Вариант_4_ru')
    option4_uz = models.CharField(max_length=30, null=True, blank=True, verbose_name='Вариант_4_uz')

    option5_ru = models.CharField(max_length=30, null=True, blank=True, verbose_name='Вариант_5_ru')
    option5_uz = models.CharField(max_length=30, null=True, blank=True, verbose_name='Вариант_5_uz')

    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Создан')

    option1_count = models.IntegerField(default=0, verbose_name='Количество варианта 1')
    option2_count = models.IntegerField(default=0, verbose_name='Количество варианта 2')
    option3_count = models.IntegerField(default=0, verbose_name='Количество варианта 3')
    option4_count = models.IntegerField(default=0, verbose_name='Количество варианта 4')
    option5_count = models.IntegerField(default=0, verbose_name='Количество варианта 5')

    def total(self):
        return self.option1_count + self.option2_count + self.option3_count + self.option4_count + self.option5_count

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.pk}'


class EmployeeResponse(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    question_text = models.TextField(null=True, blank=True, verbose_name='Вопрос')
    response = models.TextField(null=True, blank=True, verbose_name='Ответ')
    response_option = models.CharField(max_length=30, null=True, blank=True, verbose_name='Вариант ответа')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Отдел')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    survey_id = models.CharField(max_length=40, null=True, blank=True, verbose_name='ID ответа')

    class Meta:
        verbose_name = "Ответ сотрудника"
        verbose_name_plural = 'Ответы сотрудников'


class SurveyCompletion(models.Model):
    survey_id = models.CharField(max_length=40, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        unique_together = ('survey_id', 'department')

    def str(self):
        return f"{self.survey_id} - {self.department.name}"
