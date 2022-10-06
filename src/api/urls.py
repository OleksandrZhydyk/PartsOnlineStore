from django.urls import include, path
from rest_framework import routers

from api.views import (ModelDeleteView, ModelListCreateView, ModelRetrieveView,
                       ModelUpdateView, PartDeleteView, PartListCreateView,
                       PartRetrieveView, PartUpdateView, UserViewSet)

router = routers.DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("", include(router.urls)),
    path("part/", PartListCreateView.as_view()),
    path("part/<str:part_number>/", PartRetrieveView.as_view()),
    path("part/<str:part_number>/delete/", PartDeleteView.as_view()),
    path("part/<str:part_number>/update/", PartUpdateView.as_view()),
    path("model/", ModelListCreateView.as_view()),
    path("model/<str:model>/", ModelRetrieveView.as_view()),
    path("model/<str:model>/delete/", ModelDeleteView.as_view()),
    path("model/<str:model>/update/", ModelUpdateView.as_view()),
]
