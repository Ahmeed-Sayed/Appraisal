# Generated by Django 4.2.8 on 2023-12-24 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HrEmployeeMore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empDirectHead', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hrDirectHead', to='accounts.directhead')),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='employeemore',
            name='departmentManager',
        ),
        migrations.AlterField(
            model_name='employeemore',
            name='empDirectHead',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employeedirectHead', to='accounts.directhead'),
        ),
        migrations.DeleteModel(
            name='DirectHeadMore',
        ),
    ]
