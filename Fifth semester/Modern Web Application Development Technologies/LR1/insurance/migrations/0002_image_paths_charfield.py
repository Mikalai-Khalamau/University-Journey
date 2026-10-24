from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("insurance", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newsarticle",
            name="image_url",
            field=models.CharField(
                blank=True,
                help_text="https://… or static path insurance/images/…",
                max_length=500,
            ),
        ),
        migrations.AlterField(
            model_name="contactperson",
            name="photo_url",
            field=models.CharField(
                blank=True,
                help_text="https://… or static path insurance/images/…",
                max_length=500,
            ),
        ),
    ]
