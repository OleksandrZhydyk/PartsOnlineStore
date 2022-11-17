from django.urls import path

from accounts.views import (LoginUser, LogoutUser, create_comment,
                            generate_user, update_profile)

urlpatterns = [
    path("<int:count>/", generate_user, name="generate_user"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", LogoutUser.as_view(), name="logout"),
    path("profile/<uuid:pk>/", update_profile, name="user_profile"),
    path("comment/<str:part_number>/", create_comment, name="create_comment"),
]
