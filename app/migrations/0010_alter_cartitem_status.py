# Generated by Django 3.2 on 2022-07-21 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20220721_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='status',
            field=models.CharField(
                choices=[('C', 'Created Order'), ('W', 'Waiting')], default='W', max_length=1,
            ),
        ),
    ]