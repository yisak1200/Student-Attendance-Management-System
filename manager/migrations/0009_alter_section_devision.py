# Generated by Django 5.0.2 on 2024-05-27 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_course_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='devision',
            field=models.CharField(blank=True, choices=[('Regular', 'Regular'), ('Extension', 'Extension')], max_length=50, null=True),
        ),
    ]
