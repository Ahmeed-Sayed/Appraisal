# Generated by Django 4.2.8 on 2024-01-05 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_alter_departmentmanagermore_manageddepartment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupObjective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('objectivePerspective', models.CharField(choices=[('Financial', 'Financial'), ('Customer', 'Customer'), ('Process Improvement', 'Process Improvement'), ('People', 'People')], max_length=255)),
                ('weight', models.FloatField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupObjective', to='accounts.department')),
            ],
        ),
        migrations.CreateModel(
            name='GroupObjectiveInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actualDate', models.DateField()),
                ('evidence', models.TextField(max_length=500)),
                ('file', models.FileField(upload_to='evidence/')),
                ('directHeadReview', models.BooleanField(default=False)),
                ('departmentManagerReview', models.BooleanField(default=False)),
                ('hrReview', models.BooleanField(default=False)),
                ('creationDate', models.DateField(default=django.utils.timezone.now)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groubObjectiveInstance', to='accounts.employee')),
            ],
        ),
        migrations.CreateModel(
            name='ObjectivePerspectiveBlueprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objectivePerspective', models.CharField(choices=[('Financial', 'Financial'), ('Customer', 'Customer'), ('Process Improvement', 'Process Improvement'), ('People', 'People')], max_length=255)),
                ('target', models.IntegerField(blank=True, null=True)),
                ('targetDate', models.DateField(blank=True, null=True)),
                ('monitoringFrequency', models.CharField(choices=[('Yearly', 'Yearly'), ('Quarterly', 'Quarterly'), ('Monthly', 'Monthly')], max_length=255)),
                ('objectiveDescription', models.TextField()),
                ('kpiMeasure', models.TextField()),
                ('weight', models.FloatField()),
                ('instanceCount', models.IntegerField(blank=True, default=0, null=True)),
                ('totalInstances', models.IntegerField(blank=True, default=0, null=True)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=6)),
                ('creationDate', models.DateField(default=django.utils.timezone.now)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Blueprint', to='accounts.employee')),
                ('groupObjective', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blueprint', to='core.groupobjective')),
            ],
        ),
        migrations.CreateModel(
            name='InstanceNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, null=True)),
                ('groubObjectiveInstance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='note', to='core.groupobjectiveinstance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instanceNote', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlueprintObjectiveInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blueprint', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='BlueprintInstance', to='core.objectiveperspectiveblueprint')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='BlueprintInstance', to='accounts.employee')),
                ('objectiveInstance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='BlueprintInstance', to='core.groupobjectiveinstance')),
            ],
        ),
    ]
