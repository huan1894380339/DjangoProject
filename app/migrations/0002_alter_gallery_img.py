# Generated by Django 3.2 on 2022-05-16 08:25

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gallery",
            name="img",
            field=models.ImageField(
                storage=gdstorage.storage.GoogleDriveStorage(),
                upload_to="maps/",
            ),
        ),
    ]
