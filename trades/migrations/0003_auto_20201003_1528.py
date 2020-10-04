# Generated by Django 3.1 on 2020-10-03 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0002_auto_20201003_1405'),
    ]

    operations = [
        migrations.RenameField(
            model_name='condition',
            old_name='related_round',
            new_name='related_step',
        ),
        migrations.AddField(
            model_name='trade',
            name='status',
            field=models.IntegerField(choices=[(0, 'active'), (1, 'waiting for cancellation approval'), (2, 'judgement'), (3, 'cancelled')], default=0),
        ),
    ]