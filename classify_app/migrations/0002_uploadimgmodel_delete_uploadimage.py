# Generated by Django 4.1.2 on 2022-11-07 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classify_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadImgModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
        migrations.DeleteModel(
            name='UploadImage',
        ),
    ]
