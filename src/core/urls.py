from django.urls import path

from core.views import index_view, get_parts_view, get_part_detail

urlpatterns = [
    path("", index_view, name="index"),
    path("parts/", get_parts_view, name="parts_view"),
    path("parts_detail/<str:part_number>/", get_part_detail, name='part_detail'),
]
