from django.urls import path

from accounts.views import generate_user, LoginUser, LogoutUser, UserProfile

urlpatterns = [
    path("<int:count>/", generate_user, name="generate_user"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", LogoutUser.as_view(), name="logout"),
    path("profile/<uuid:pk>/", UserProfile.as_view(), name="user_profile"),
]
