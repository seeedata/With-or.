# Generated by Django 3.1.3 on 2024-08-22 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recruitment', '0010_remove_question_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='team_name',
        ),
        migrations.AddField(
            model_name='answer',
            name='isteam',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
