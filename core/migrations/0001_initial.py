# Generated by Django 4.2.8 on 2023-12-24 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_hremployeemore_remove_employeemore_departmentmanager_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Objectives',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Appraisal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('kpis', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('targetDate', models.DateField()),
                ('actualDate', models.DateField(blank=True, null=True)),
                ('empSubmission', models.BooleanField(default=False)),
                ('directHeadSubmission', models.BooleanField(default=False)),
                ('departmentManagerSubmission', models.BooleanField(default=False)),
                ('departmentManager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appraisalDepartmentManager', to='accounts.departmentmanager')),
                ('directHead', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appraisalDirectHead', to='accounts.directhead')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appraisalEmployee', to='accounts.employee')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appraisalObject', to='core.objectives')),
            ],
        ),
    ]