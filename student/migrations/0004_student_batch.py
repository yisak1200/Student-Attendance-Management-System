# Generated by Django 5.0.2 on 2024-05-27 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_semester_is_visible'),
        ('student', '0003_remove_student_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='manager.batch'),
        ),
    ]
