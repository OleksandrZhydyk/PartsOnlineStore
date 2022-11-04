from django.urls import path

from core.views import index_view, generate_shops

urlpatterns = [
    path("", index_view, name="index"),
    path("generate_shops/<int:count>/", generate_shops, name="generate_shops")
]
