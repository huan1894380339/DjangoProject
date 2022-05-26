# Generated by Django 3.2 on 2022-05-24 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_cartitem_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='order',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='orderitem', to='app.order',
            ),
        ),
    ]