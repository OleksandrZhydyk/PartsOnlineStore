from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config import settings

urlpatterns = [
    path("", include("core.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("mongo/", include("mongo.urls")),
]

# if settings.dev.DEBUG:
#     urlpatterns += static(settings.dev.MEDIA_URL, document_root=settings.dev.MEDIA_ROOT)
#     urlpatterns += static(settings.dev.STATIC_URL, document_root=settings.dev.STATIC_ROOT)
