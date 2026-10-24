from django.db import migrations


def forwards(apps, schema_editor):
    NewsArticle = apps.get_model("insurance", "NewsArticle")
    ContactPerson = apps.get_model("insurance", "ContactPerson")
    for i, article in enumerate(NewsArticle.objects.all().order_by("id")):
        url = (article.image_url or "").strip()
        if not url or "picsum.photos" in url:
            article.image_url = f"insurance/images/news_{(i % 3) + 1}.svg"
            article.save(update_fields=["image_url"])
    for person in ContactPerson.objects.all():
        url = (person.photo_url or "").strip()
        if not url or "picsum.photos" in url:
            person.photo_url = "insurance/images/contact.svg"
            person.save(update_fields=["photo_url"])


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("insurance", "0002_image_paths_charfield"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
