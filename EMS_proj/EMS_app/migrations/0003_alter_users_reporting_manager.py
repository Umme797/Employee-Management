# Generated by Django 5.1.6 on 2025-02-08 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS_app', '0002_manager_remove_users_reporting_manager_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='reporting_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='EMS_app.users'),
        ),
    ]
