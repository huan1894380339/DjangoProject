# Generated by Django 3.2 on 2022-07-21 03:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20220721_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='status',
            field=models.CharField(
                choices=[('C', 'Created Order'), ('W', 'Waiting')], default='W', max_length=1,
            ),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(
                limit_choices_to={
                    'user_cart__isnull': False,
                }, on_delete=django.db.models.deletion.CASCADE, related_name='user_cart', to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]