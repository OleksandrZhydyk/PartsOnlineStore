from django.urls import path

from core.views import generate_shops, index_view

urlpatterns = [
    path("", index_view, name="index"),
    path("generate_shops/<int:count>/", generate_shops, name="generate_shops"),
]
