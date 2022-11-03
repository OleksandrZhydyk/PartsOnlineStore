import random
from faker import Faker

from django.shortcuts import render

from accounts.models import Comment
from catalogue.models import MachineModel, Part
from config import settings
from core.models import Shop


def index_view(request):
    shops_location = Shop.objects.values_list("location", "address")
    coordinates = []
    for index, location in enumerate(shops_location):
        coordinates.append({})
        coordinates[index]["latitude"], coordinates[index]["longitude"] = location[0].split(",")
    return render(
        request,
        template_name="index.html",
        context={
            "title": "Main page",
            "data": coordinates,
            "google_maps_api_key": settings.base.GOOGLE_MAPS_API_KEY,
            "addresses": list(shops_location),
        },
    )


def get_parts_view(request):
    parts = Part.objects.all()
    models = MachineModel.objects.all()

    if "search" in request.GET:
        field = request.GET.get("field")
        search = request.GET.get("search")
        parts = parts.filter(**{f"{field}__icontains": f"{search}"})

    if "machine_model" in request.GET:
        value_list = request.GET.getlist("machine_model")
        parts = parts.filter(machine_model__model__in=value_list).distinct()
    if "machine_system" in request.GET:
        value_list = request.GET.getlist("machine_system")
        parts = parts.filter(machine_system__in=value_list).distinct()
    models = models.filter(part__in=parts).distinct()
    machine_systems = parts.distinct("machine_system")
    return render(
        request,
        template_name="parts_view.html",
        context={"title": "Filtered parts", "parts": parts, "models": models, "machine_system": machine_systems},
    )


def get_part_detail(request, **kwargs):
    part = Part.objects.get(part_number=kwargs.get("part_number"))
    shops = Shop.objects.filter(part=kwargs.get("part_number"))
    comments = Comment.objects.filter(part=kwargs.get("part_number"))
    return render(
        request,
        template_name="part_detail.html",
        context={"title": "Part detail", "part": part, "shops": shops, "comments": comments},
    )


# def add_to_cart(request, **kwargs):
#     print(kwargs)
#     CartItem.objects.create(part=kwargs.get('part_number'), quantity=kwargs.get('quantity')),
#                             # cart_id=kwargs.get('user_cart'))
# return HttpResponseRedirect(reverse("parts"))

# return render(request, template_name="students_create.html", context={"response": response})
#
#
# from PIL import Image, ImageDraw, ImageFont
#
# width = 512
# height = 512
# message = "Hello boss!"
# img = Image.new('RGB', (width, height), color='blue')
#
# imgDraw = ImageDraw.Draw(img)
#
# imgDraw.text((10, 10), message, fill=(255, 255, 0))
#
# img.save('result.png')

# def generate_shops(cls, count=1):
#     faker = Faker("uk_UA")
#     for _ in range(count):
#         cls.objects.create(
#             address=faker.address(),
#             part=[]
#         )

# def gen_part_number():
#     prefix = ["AL", "R", "RE", "AX", "AH", "AXE"]
#     return prefix[random.randint(0, 5)]+str(random.randint(1000, 100000))
#
# def generate_parts(cls, count=1):
#
#     for _ in range(count):
#         cls.objects.create(
#             part_number=gen_part_number(),
#             part_name=
#             price=random.uniform(5, 500),
#             discount_price=random.uniform(0, 0.9),
#             image=
#             description=
#             stock_quantity=random.randint(1, 100),
#             machine_system=random.randint(1, 8),
#         )

