# Generated by Django 5.1.4 on 2024-12-29 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='year',
            field=models.CharField(help_text='Enter the year', max_length=4),
        ),
    ]