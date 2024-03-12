from django.urls import path
from auth.views import RegisterView, TokenObtainPairView, ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpattern = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_obtain_pair"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("change_password/<str:pk>/", ChangePasswordView.as_view(), name="change_password")
]