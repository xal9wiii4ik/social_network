# Generated by Django 3.1.5 on 2021-03-05 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('followers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follower',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Subscriber',
        ),
    ]
