# Generated by Django 3.1.5 on 2021-02-21 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20210220_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislike',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name='Дизлайк'),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Фотография'),
        ),
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name='Лайк'),
        ),
    ]
