# Generated by Django 4.1.2 on 2022-11-15 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classify_app', '0006_uploadimgmodel_success_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadimgmodel',
            name='square_number',
            field=models.IntegerField(default=0),
        ),
    ]
