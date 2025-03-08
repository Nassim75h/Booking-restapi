from django.contrib.postgres.fields.array import lookups
from django.urls import path

from . import views
# NOTE : i had to add this since as_view and Models are made to be the usual implementation !
profile_view = views.ProfileView.as_view(
    {"get": "retrieve", "put": "update",
        "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("register/", views.UserRegisterView.as_view()),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("token/refresh/",views.RefreshAccessToken.as_view()),
    path("profile/", profile_view, name="profile"),
    path(
        "changepassword/", views.UserChangePasswordView.as_view(), name="changepassword"
    ),
    path(
        "credential/request-reset-password/",
        views.SendPasswordResetEmailView.as_view(),
        name="sendresetpasswordemail",
    ),
    path(
        "credential/reset-password/",
        views.ResetPasswordView.as_view(),
        name="resetpassword",
    ),
]
