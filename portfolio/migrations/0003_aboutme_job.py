# Generated by Django 5.1.4 on 2024-12-30 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_project_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutme',
            name='job',
            field=models.CharField(default=1, help_text='Enter your job. E.g.: Software Engineer', max_length=100),
            preserve_default=False,
        ),
    ]