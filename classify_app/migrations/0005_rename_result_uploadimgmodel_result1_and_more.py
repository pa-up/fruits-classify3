# Generated by Django 4.1.2 on 2022-11-14 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classify_app', '0004_delete_cvimgmodel_uploadimgmodel_result_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadimgmodel',
            old_name='result',
            new_name='result1',
        ),
        migrations.AddField(
            model_name='uploadimgmodel',
            name='result10',
            field=models.ImageField(default=models.ImageField(upload_to='documents/'), upload_to='results/'),
        ),
        migrations.AddField(
            model_name='uploadimgmodel',
            name='result11',
            field=models.ImageField(default=models.ImageField(upload_to='documents/'), upload_to='results/'),
        ),
        migrations.AddField(
            model_name='uploadimgmodel',
            name='result12',
            field=models.ImageField(default=models.ImageField(upload_to='documents/'), upload_to='results/'),
        ),
        migrations.AddField(
            model_name='uploadimgmodel',
            name='result13',
            field=models.ImageField(default=models.ImageField(upload_to='documents/'), upload_to='results/'),
        ),
        migrations.AddField(
            model_name='uploadimgmodel',
            name='result2',
            field=models.ImageField(default=models.ImageField(upload_to='documents/'), upload_to='results/'),
        ),
        migrations.AddField(
            model_name='uploadimgmodel',
            name='result3',
            field=models.ImageField(default=models.ImageField(upload_to='documents/'), upload_to='results/'),
        ),
        migrations.AddField(
            model_name='uploadimgmodel',
            name='result4',
            field=models.ImageField(default=models.ImageField(upload_to='documents/'), upload_to='results/'),
        ),
        migrations.AddField(
            model_name='uploadimgmodel',
            name='result5',
            field=models.ImageField(default=models.ImageField(upload_to='documents/'), upload_to='results/'),
        ),
        migrations.AddField(
            model_name='uploadimgmodel',
            name='result6',
            field=models.ImageField(default=models.ImageField(upload_to='documents/'), upload_to='results/'),
        ),
        migrations.AddField(
            model_name='uploadimgmodel',
            name='result7',
            field=models.ImageField(default=models.ImageField(upload_to='documents/'), upload_to='results/'),
        ),
        migrations.AddField(
            model_name='uploadimgmodel',
            name='result8',
            field=models.ImageField(default=models.ImageField(upload_to='documents/'), upload_to='results/'),
        ),
        migrations.AddField(
            model_name='uploadimgmodel',
            name='result9',
            field=models.ImageField(default=models.ImageField(upload_to='documents/'), upload_to='results/'),
        ),
        migrations.AlterField(
            model_name='uploadimgmodel',
            name='title',
            field=models.CharField(default='title', max_length=50),
        ),
    ]
