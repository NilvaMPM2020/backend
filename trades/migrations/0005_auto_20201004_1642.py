# Generated by Django 3.1 on 2020-10-04 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0004_judge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='decision',
            field=models.IntegerField(choices=[(-1, 'business party'), (1, 'client party')]),
        ),
    ]
