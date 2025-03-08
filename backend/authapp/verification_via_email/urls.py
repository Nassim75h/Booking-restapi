from django.urls import path
from .. import views

urlpatterns = [
    path('activate/<str:token>/',
         views.ActivateAccountView.as_view(), name='activateaccount'),
    path(
        "reset-password/<str:token>/",
        views.TempValidateRequestResetPassLink.as_view(),
        name="resetpassword",
    ),
]
