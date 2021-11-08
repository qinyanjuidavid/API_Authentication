from django.urls import path
from authentication import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)

from authentication.views import MyTokenObtainPairView, VerifyEmail

urlpatterns = [
    path('', views.RegisterApiview),
    path('token/', MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('activate/', VerifyEmail.as_view(), name="email-verify"),
    path('user/', views.authenticatedUser),

]

# {
#     "email": "test6@gmail.com",
#     "username": "test6",
#     "password": "kinyanjuid29",
#     "password_confirmation": "kinyanjuid29"
# }
