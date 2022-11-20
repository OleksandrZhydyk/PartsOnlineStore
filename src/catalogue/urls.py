from django.urls import path

from catalogue.views import (generate_machine_models, generate_parts,
                             get_part_detail, get_parts_view)

urlpatterns = [
    path("parts/", get_parts_view, name="parts_view"),
    path("parts/<str:part_number>/", get_part_detail, name="part_detail"),
    path("generate_part/<int:count>/", generate_parts, name="generate_parts"),
    path("generate_model/<int:count>/", generate_machine_models, name="generate_machine_models"),
]
