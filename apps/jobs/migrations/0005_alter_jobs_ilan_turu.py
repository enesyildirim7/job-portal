# Generated by Django 4.1.2 on 2022-10-29 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0004_uuidtaggeditem_alter_jobs_etiketler"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobs",
            name="ilan_turu",
            field=models.IntegerField(
                choices=[(0, "Freelance"), (1, "Yarı Zamanlı"), (2, "Tam Zamanlı")],
                default=2,
                verbose_name="İlan Türü",
            ),
        ),
    ]