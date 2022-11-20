from celery import shared_task
from faker import Faker

from accounts.models import CustomUser


@shared_task
def create_user(count=1):
    faker = Faker()
    for _ in range(count):
        email_password = faker.email()
        user = CustomUser.objects.create(
            email=email_password,
            first_name=faker.first_name(),
            last_name=faker.last_name(),
        )
        user.set_password(email_password)
        user.save()
