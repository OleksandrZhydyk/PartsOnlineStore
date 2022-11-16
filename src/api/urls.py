from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api.views import (ModelCreateView, ModelDeleteView, ModelListView,
                       ModelRetrieveView, ModelUpdateView,
                       PartCreateView, PartDeleteView, PartListView,
                       PartRetrieveView, PartUpdateView, ProfileUserUpdateView,
                       ProfileUserView, ShopListView,
                       ShopRetrieveUpdateDeleteView, UserViewSet)

router = routers.DefaultRouter()
router.register("users", UserViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Quizez API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger_docs"),
    path("", include(router.urls)),
    path("users/profile/<uuid:pk>/", ProfileUserView.as_view(), name="profile_retrieve"),
    path("users/profile/<uuid:pk>/", ProfileUserUpdateView.as_view(), name="profile_update"),
    path(
        "part/",
        PartListView.as_view(),
        name="parts_list",
    ),
    path("part/create/", PartCreateView.as_view(), name="part_create"),
    path("part/<str:part_number>/", PartRetrieveView.as_view(), name="part_retrieve"),
    path("part/<str:part_number>/delete/", PartDeleteView.as_view(), name="part_delete"),
    path("part/<str:part_number>/update/", PartUpdateView.as_view(), name="part_update"),
    path("model/", ModelListView.as_view(), name="models_retrieve"),
    path("model/create/", ModelCreateView.as_view(), name="model_create"),
    path("model/<str:model>/", ModelRetrieveView.as_view(), name="model_retrieve"),
    path("model/<str:model>/delete/", ModelDeleteView.as_view(), name="model_delete"),
    path("model/<str:model>/update/", ModelUpdateView.as_view(), name="model_update"),
    path("shop/", ShopListView.as_view(), name="shops_list"),
    path("shop/<int:pk>/", ShopRetrieveUpdateDeleteView.as_view(), name="shop_crud"),
]
