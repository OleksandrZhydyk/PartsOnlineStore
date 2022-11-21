from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from accounts.models import Comment
from catalogue.models import MachineModel, Part
from catalogue.tasks import create_machine_model, create_part
from core.models import Shop


@login_required
def generate_parts(request, **kwargs):
    if request.user.is_staff:
        count = kwargs.get("count")
        create_part(count)
        message = "Part created"
        return render(
            request,
            template_name="catalogue/generate_data.html",
            context={"title": "Generate part", "message": message},
        )
    else:
        return render(request,
                      template_name="core/forbidden.html",
                      context={"title": "Forbidden"})


@login_required
def generate_machine_models(request, **kwargs):
    if request.user.is_staff:
        count = kwargs.get("count")
        create_machine_model(count)
        message = "Machine model created"
        return render(
            request,
            template_name="catalogue/generate_data.html",
            context={"title": "Generate part", "message": message},
        )
    else:
        return render(request,
                      template_name="core/forbidden.html",
                      context={"title": "Forbidden"})


def get_parts_view(request):
    parts = Part.objects.all()
    models = MachineModel.objects.all()
    machine_systems = Part.MACHINE_SYSTEMS
    checked_models = []
    checked_systems = []

    if "search" in request.GET:
        field = request.GET.get("field")
        search = request.GET.get("search")
        if field == "machine_model":
            parts = parts.filter(**{f"{field}__model__icontains": f"{search}"})
        else:
            parts = parts.filter(**{f"{field}__icontains": f"{search}"})

    if "machine_model" in request.GET:
        value_list = request.GET.getlist("machine_model")
        parts = parts.filter(machine_model__model__in=value_list).distinct()
        checked_models = value_list

    if "machine_system" in request.GET:
        value_list = request.GET.getlist("machine_system")
        parts = parts.filter(machine_system__in=value_list).distinct()
        checked_systems = value_list

    if "part_name" in request.GET:
        part_name = request.GET["part_name"]
        parts = parts.filter(part_name=part_name)

    paginator = Paginator(parts, 5)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        template_name="catalogue/parts_view.html",
        context={"title": "Filtered parts", "models": models,
                 "machine_systems": machine_systems, "checked_models": checked_models,
                 "checked_systems": checked_systems, "page_obj": page_obj},
    )


def get_part_detail(request, **kwargs):
    part_number = kwargs.get("part_number")
    part = Part.objects.get(part_number=part_number)
    shops = Shop.objects.filter(part=part)
    comments = Comment.objects.filter(part=part).order_by("-created")
    models = MachineModel.objects.filter(part=part)
    return render(
        request,
        template_name="catalogue/part_detail.html",
        context={"title": "Part detail", "part": part,
                 "shops": shops, "comments": comments, "models": models},
    )

