from django.urls import path
from authentication import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)

from authentication.views import MyTokenObtainPairView

urlpatterns = [
    path('', views.RegisterApiview),
    path('token/', MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]
