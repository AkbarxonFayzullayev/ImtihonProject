# Generated by Django 5.2 on 2025-05-03 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_alter_student_fullname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='fullname',
            field=models.CharField(default='Unknown Student', max_length=50),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='fullname',
            field=models.CharField(default='Unknown Teacher', max_length=50),
        ),
    ]
