from django.urls import path

from accounts.views import (activate_user, create_comment, generate_user,
                            login_user, logout_user, signup, update_profile)

urlpatterns = [
    path("<int:count>/", generate_user, name="generate_user"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("signup/", signup, name="signup"),
    path("activate/<str:uuid64>/<str:token>/", activate_user, name="activate_user"),
    path("profile/<uuid:pk>/", update_profile, name="user_profile"),
    path("comment/<str:part_number>/", create_comment, name="create_comment"),
]
