from celery import shared_task
from faker import Faker

from catalogue.models import Part
from core.models import Shop


@shared_task
def create_shops(count=1):
    faker = Faker("uk_UA")

    for _ in range(count):
        address = faker.address()
        location = ",".join(faker.local_latlng(country_code='UA')[0:2])
        shop = Shop.objects.create(
            address=address,
            location=location,
        )
        shop.part.set(Part.objects.filter(price__gte=100))
