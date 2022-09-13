from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterAPIView, LogOutAPI, activate

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('logout/', LogOutAPI.as_view()),
    path('activate/<str:activation_code>/', activate),
 ]