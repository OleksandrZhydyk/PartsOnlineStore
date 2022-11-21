from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from config import settings
from core.models import Shop
from core.tasks import create_shops


def index_view(request):
    shops_location = Shop.objects.values_list("location", "address")
    coordinates = []
    for index, location in enumerate(shops_location):
        coordinates.append({})
        coordinates[index]["latitude"], coordinates[index]["longitude"] = location[0].split(",")
    return render(
        request,
        template_name="core/index.html",
        context={
            "title": "Main page",
            "data": coordinates,
            "google_maps_api_key": settings.base.GOOGLE_MAPS_API_KEY,
            "addresses": list(shops_location),
        },
    )


def page_not_found_view(request, exception):
    return render(request, template_name="core/404.html",
                  context={"title": "Page not found"})


def unauthorized_view(request, exception):
    return render(request, template_name="core/forbidden.html",
                  context={"title": "Forbidden"})


@login_required
def generate_shops(request, **kwargs):
    if request.user.is_staff:
        count = kwargs.get("count")
        create_shops(count)
        message = "Shop created"
        return render(
            request,
            template_name="catalogue/generate_data.html",
            context={"title": "Generate part", "message": message},
        )
    else:
        return render(request,
                      template_name="core/forbidden.html",
                      context={"title": "Forbidden"})
