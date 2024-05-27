# Generated by Django 4.2.1 on 2024-05-22 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0008_remove_questions_option1_remove_questions_option2_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="questions",
            name="question_text_ru",
        ),
        migrations.RemoveField(
            model_name="questions",
            name="question_text_uz",
        ),
        migrations.AddField(
            model_name="questions",
            name="question_ru",
            field=models.TextField(
                blank=True, max_length=200, null=True, verbose_name="Вопрос ru"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="question_uz",
            field=models.TextField(
                blank=True, max_length=200, null=True, verbose_name="Вопрос uz"
            ),
        ),
        migrations.AlterField(
            model_name="questions",
            name="option1_ru",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант_1_ru"
            ),
        ),
        migrations.AlterField(
            model_name="questions",
            name="option1_uz",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант_1_uz"
            ),
        ),
        migrations.AlterField(
            model_name="questions",
            name="option2_ru",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант_2_ru"
            ),
        ),
        migrations.AlterField(
            model_name="questions",
            name="option2_uz",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант_2_uz"
            ),
        ),
        migrations.AlterField(
            model_name="questions",
            name="option3_ru",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант_3_ru"
            ),
        ),
        migrations.AlterField(
            model_name="questions",
            name="option3_uz",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант_3_uz"
            ),
        ),
        migrations.AlterField(
            model_name="questions",
            name="option4_ru",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант_4_ru"
            ),
        ),
        migrations.AlterField(
            model_name="questions",
            name="option4_uz",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант_4_uz"
            ),
        ),
        migrations.AlterField(
            model_name="questions",
            name="option5_ru",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант_5_ru"
            ),
        ),
        migrations.AlterField(
            model_name="questions",
            name="option5_uz",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вариант_5_uz"
            ),
        ),
    ]