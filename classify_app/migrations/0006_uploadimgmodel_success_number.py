# Generated by Django 4.1.2 on 2022-11-14 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classify_app', '0005_rename_result_uploadimgmodel_result1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadimgmodel',
            name='success_number',
            field=models.IntegerField(default=0),
        ),
    ]
