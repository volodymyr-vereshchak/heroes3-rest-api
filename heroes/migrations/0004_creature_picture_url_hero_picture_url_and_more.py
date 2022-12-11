# Generated by Django 4.1.4 on 2022-12-11 10:55

from django.db import migrations, models
import heroes.models


class Migration(migrations.Migration):

    dependencies = [
        ("heroes", "0003_rename_seondary_skill_first_hero_secondary_skill_first"),
    ]

    operations = [
        migrations.AddField(
            model_name="creature",
            name="picture_url",
            field=models.ImageField(null=True, upload_to=heroes.models.image_file_path),
        ),
        migrations.AddField(
            model_name="hero",
            name="picture_url",
            field=models.ImageField(null=True, upload_to=heroes.models.image_file_path),
        ),
        migrations.AddField(
            model_name="resource",
            name="picture_url",
            field=models.ImageField(null=True, upload_to=heroes.models.image_file_path),
        ),
        migrations.AddField(
            model_name="secondaryskill",
            name="picture_url",
            field=models.ImageField(null=True, upload_to=heroes.models.image_file_path),
        ),
        migrations.AddField(
            model_name="spell",
            name="picture_url",
            field=models.ImageField(null=True, upload_to=heroes.models.image_file_path),
        ),
        migrations.AddField(
            model_name="town",
            name="picture_url",
            field=models.ImageField(null=True, upload_to=heroes.models.image_file_path),
        ),
    ]
