# Generated by Django 3.2 on 2022-07-06 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20220706_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='status',
            field=models.CharField(
                choices=[('C', 'Created Order'), ('W', 'Waiting')], default='N', max_length=1,
            ),
        ),
    ]
