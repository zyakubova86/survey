# Generated by Django 4.2.1 on 2024-05-22 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0009_remove_questions_question_text_ru_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employeeresponse",
            name="response",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Ответ"
            ),
        ),
    ]
