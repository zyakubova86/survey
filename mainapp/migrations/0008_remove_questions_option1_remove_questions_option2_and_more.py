# Generated by Django 4.2.1 on 2024-05-22 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0007_employeeresponse"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="questions",
            name="option1",
        ),
        migrations.RemoveField(
            model_name="questions",
            name="option2",
        ),
        migrations.RemoveField(
            model_name="questions",
            name="option3",
        ),
        migrations.RemoveField(
            model_name="questions",
            name="option4",
        ),
        migrations.RemoveField(
            model_name="questions",
            name="option5",
        ),
        migrations.RemoveField(
            model_name="questions",
            name="question_text",
        ),
        migrations.AddField(
            model_name="questions",
            name="option1_ru",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант 1 (ру)"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="option1_uz",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант 1 (уз)"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="option2_ru",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант 2 (ру)"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="option2_uz",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант 2 (уз)"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="option3_ru",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант 3 (ру)"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="option3_uz",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант 3 (уз)"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="option4_ru",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант 4 (ру)"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="option4_uz",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант 4 (уз)"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="option5_ru",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант 5 (ру)"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="option5_uz",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант 5 (уз)"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="question_text_ru",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Вопрос (ру)"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="question_text_uz",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Вопрос (уз)"
            ),
        ),
    ]