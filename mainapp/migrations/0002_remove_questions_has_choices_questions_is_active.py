# Generated by Django 4.2.1 on 2024-05-15 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="questions",
            name="has_choices",
        ),
        migrations.AddField(
            model_name="questions",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Активен"),
        ),
    ]
