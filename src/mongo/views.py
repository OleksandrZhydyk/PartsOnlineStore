from mongo.models import Customer, Basket
from django.http import HttpResponse
from faker import Faker


def create_mongo_data(request):
    baskets = [Basket(part='RE12345' + str(i), price=100/i) for i in range(1, 5)]
    fake = Faker()
    saved = Customer(
        name=fake.first_name(),
        email=fake.email(),
        baskets=baskets
    ).save()
    return HttpResponse(f"{saved}")


def view_mongo_data(request):
    baskets = Customer.objects.all().values_list('baskets')
    return HttpResponse(f"{[basket for basket in baskets]}")





