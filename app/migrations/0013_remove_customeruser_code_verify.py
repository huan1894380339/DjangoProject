# Generated by Django 3.2 on 2022-05-26 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_customeruser_code_verify'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customeruser',
            name='code_verify',
        ),
    ]
