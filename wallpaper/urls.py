from django.urls import path, include

from .views import LikeAPIView, RatingAPIView, \
    CelerySendToEmailAPIView

urlpatterns = [
    path('like/<int:pk>/', LikeAPIView.as_view()),
    path('rating/<int:pk>/', RatingAPIView.as_view()),
    path('celery/', CelerySendToEmailAPIView.as_view()),
 ]