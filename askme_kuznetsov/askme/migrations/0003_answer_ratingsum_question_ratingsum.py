# Generated by Django 4.2 on 2023-05-23 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0002_alter_answer_question_ratinganswers'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='ratingsum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='ratingsum',
            field=models.IntegerField(default=0),
        ),
    ]
