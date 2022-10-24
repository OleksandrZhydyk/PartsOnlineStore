import json

from django.shortcuts import render  # NOQA

from config import settings
from core.models import Shop


def index_view(request):
    shops_location = Shop.objects.values_list('location', 'address')
    coordinates = []
    for index, location in enumerate(shops_location):
        coordinates.append({})
        coordinates[index]['latitude'], coordinates[index]['longitude'] = location[0].split(",")
    return render(request, template_name='index.html',
                  context={"title": "Main page", "data": coordinates, 'google_maps_api_key': settings.dev.GOOGLE_MAPS_API_KEY,
                           "addresses": list(shops_location)})
