# Generated by Django 5.0.2 on 2024-05-19 12:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_alter_section_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='manager.batch'),
        ),
    ]
