# Generated by Django 5.1 on 2024-12-26 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0006_alter_appointment_options_workinghours'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ['create_date']},
        ),
        migrations.AlterModelOptions(
            name='workinghours',
            options={'verbose_name': 'Working hour', 'verbose_name_plural': 'Working hours'},
        ),
        migrations.AlterField(
            model_name='workinghours',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_hours', to='doctor.doctor'),
        ),
    ]
