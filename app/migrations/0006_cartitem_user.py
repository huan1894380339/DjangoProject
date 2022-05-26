# Generated by Django 3.2 on 2022-05-24 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_cartitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
