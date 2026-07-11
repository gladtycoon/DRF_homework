from django.urls import path
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (CheckPaymentStatusView, PaymentsCreateAPIView,
                         UserCreateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("payments/", PaymentsCreateAPIView.as_view(), name="payments"),
    path(
        "success/", TemplateView.as_view(template_name="success.html"), name="success"
    ),
    path(
        "payment-status/<str:session_id>/",
        CheckPaymentStatusView.as_view(),
        name="payment_status",
    ),
]
