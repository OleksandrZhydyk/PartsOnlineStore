from django.urls import path

from mongo.views import create_mongo_data, view_mongo_data

app_name = "mongo"

urlpatterns = [
    path(
        "create_mongo/",
        create_mongo_data,
    ),
    path(
        "list_mongo/",
        view_mongo_data,
    ),
]
