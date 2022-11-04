import random

from celery import shared_task
from faker import Faker
from PIL import Image, ImageDraw, ImageFont

from catalogue.models import MachineModel, Part


def get_part_pic(pic_name):
    width = 300
    height = 300
    font = ImageFont.truetype("catalogue/arial.ttf", size=60)

    img = Image.new("RGB", (width, height), color="grey")

    imgDraw = ImageDraw.Draw(img)

    textWidth, textHeight = imgDraw.textsize(pic_name, font=font)
    xText = (width - textWidth) / 2
    yText = (height - textHeight) / 2

    imgDraw.text((xText, yText), pic_name, font=font, fill=(255, 255, 0))

    img.save(f"media/generated_part_pic/{pic_name}.png")

    return f"generated_part_pic/{pic_name}.png"


def get_part_number():
    prefix = ["AL", "R", "RE", "AX", "AH", "AXE"]
    return prefix[random.randint(0, 5)] + str(random.randint(1000, 99999))


@shared_task
def create_part(count=1):
    faker = Faker()
    part_number = get_part_number()
    parts = ["shaft", "nut", "belt", "sprocket", "bracket", "shaft key", "lever", "bearing"]
    for _ in range(count):
        Part.objects.create(
            part_number=part_number,
            part_name=parts[random.randint(0, 7)],
            price=round(random.uniform(5, 500), 2),
            discount_price=random.uniform(0, 0.9),
            image=get_part_pic(part_number),
            description=faker.paragraph(nb_sentences=4),
            stock_quantity=random.randint(1, 100),
            machine_system=random.randint(1, 8),
        )


def get_machine_model(machine_type):
    combine_prefix = ["S", "W", "T"]
    tractor_suffix = ["B", "D", "R", "M"]
    self_propelled_sprayer_prefix = ["R", "M"]
    loaders = ["KT315-24", "KT315-26", "KT315-28", "KT315-36", "KT315-38"]
    match machine_type:
        case 1:
            return str(random.randint(100, 999)) + tractor_suffix[random.randint(0, 3)]
        case 2:
            return combine_prefix[random.randint(0, 2)] + str(random.randint(600, 695))
        case 3:
            return self_propelled_sprayer_prefix[random.randint(0, 1)] + str(random.randint(4030, 4045))
        case 4:
            return str(random.randint(7600, 8600))
        case 5:
            return loaders[random.randint(0, 4)]


@shared_task
def create_machine_model(count=1):
    for _ in range(count):
        machine_type = random.randint(1, 5)
        model = MachineModel.objects.create(
            machine_type=machine_type,
            model=get_machine_model(machine_type),
        )
        model.part.set(Part.objects.filter(stock_quantity__lte=35))
