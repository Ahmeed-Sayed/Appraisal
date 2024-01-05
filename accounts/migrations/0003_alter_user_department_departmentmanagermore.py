# Generated by Django 4.2.8 on 2024-01-01 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_hremployeemore_remove_employeemore_departmentmanager_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='accounts.department'),
        ),
        migrations.CreateModel(
            name='DepartmentManagerMore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('managedDepartment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager', to='accounts.department')),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]