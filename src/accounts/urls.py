from django.urls import path

from accounts.views import generate_user

urlpatterns = [
    path("<int:count>/", generate_user, name="generate_user"),
]
