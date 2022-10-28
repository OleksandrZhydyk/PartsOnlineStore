from django.urls import path

from core.views import get_part_detail, get_parts_view, index_view

urlpatterns = [
    path("", index_view, name="index"),
    path("parts/", get_parts_view, name="parts_view"),
    path("parts_detail/<str:part_number>/", get_part_detail, name="part_detail"),
]
