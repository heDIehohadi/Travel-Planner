from django.urls import path
from apps.accounts.views import RequestOTPView,VerifyOTPView,MeApi
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path(
        "request-otp/",
        RequestOTPView.as_view(),
        name="request-otp",),
    path(
        "verify-otp/",
        VerifyOTPView.as_view(),
        name="verify-otp"),
        path(
        "me/",
        MeApi.as_view(),
        name="me"),
    path(
    "token/refresh/",
    TokenRefreshView.as_view(),
    name="token-refresh",
    )
]