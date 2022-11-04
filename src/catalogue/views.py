from django.shortcuts import render

from accounts.models import Comment
from catalogue.models import MachineModel, Part
from catalogue.tasks import create_machine_model, create_part
from core.models import Shop


def generate_parts(request, **kwargs):
    count = kwargs.get("count")
    create_part.delay(count)
    message = "Part created"
    return render(
        request,
        template_name="catalogue/generate_data.html",
        context={"title": "Generate part", "message": message},
    )


def generate_machine_models(request, **kwargs):
    count = kwargs.get("count")
    create_machine_model.delay(count)
    message = "Machine model created"
    return render(
        request,
        template_name="catalogue/generate_data.html",
        context={"title": "Generate part", "message": message},
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
        template_name="catalogue/parts_view.html",
        context={"title": "Filtered parts", "parts": parts, "models": models, "machine_system": machine_systems},
    )


def get_part_detail(request, **kwargs):
    part = Part.objects.get(part_number=kwargs.get("part_number"))
    shops = Shop.objects.filter(part=kwargs.get("part_number"))
    comments = Comment.objects.filter(part=kwargs.get("part_number"))
    return render(
        request,
        template_name="catalogue/part_detail.html",
        context={"title": "Part detail", "part": part, "shops": shops, "comments": comments},
    )
