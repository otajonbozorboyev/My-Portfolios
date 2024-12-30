# Generated by Django 5.1.4 on 2024-12-30 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_aboutme_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter the service. E.g.: Web Development Service', max_length=100)),
                ('description', models.TextField()),
                ('icon', models.ImageField(help_text='Enter the service icon', upload_to='images/services')),
            ],
        ),
    ]