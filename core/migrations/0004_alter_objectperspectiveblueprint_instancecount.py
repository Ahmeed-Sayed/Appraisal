# Generated by Django 4.2.8 on 2023-12-31 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_objectperspectiveblueprint_groupobjectinstance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objectperspectiveblueprint',
            name='instanceCount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]