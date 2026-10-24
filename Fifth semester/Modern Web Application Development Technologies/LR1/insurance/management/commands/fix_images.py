"""Point news/contact images to bundled static SVGs (no external URLs)."""
from django.core.management.base import BaseCommand

from insurance import models


class Command(BaseCommand):
    help = "Replace picsum/empty image paths with local static insurance/images/*.svg"

    def handle(self, *args, **options):
        n_news = 0
        for i, article in enumerate(models.NewsArticle.objects.all().order_by("id")):
            url = (article.image_url or "").strip()
            if not url or "picsum.photos" in url:
                article.image_url = f"insurance/images/news_{(i % 3) + 1}.svg"
                article.save(update_fields=["image_url"])
                n_news += 1
        n_contact = 0
        for person in models.ContactPerson.objects.all():
            url = (person.photo_url or "").strip()
            if not url or "picsum.photos" in url:
                person.photo_url = "insurance/images/contact.svg"
                person.save(update_fields=["photo_url"])
                n_contact += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Updated news={n_news}, contacts={n_contact}. "
                f"Open /static/insurance/images/news_1.svg to verify static files."
            )
        )
