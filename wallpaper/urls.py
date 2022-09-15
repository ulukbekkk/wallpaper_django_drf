from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import index, WallpaperModelViewSet, CategoryModelViewSet, CommentViewSet, LikeAPIView, RatingAPIView

router = DefaultRouter()
router.register('products', WallpaperModelViewSet)
router.register('categories', CategoryModelViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('like/<int:pk>/', LikeAPIView.as_view()),
    path('rating/<int:pk>/', RatingAPIView.as_view()),
    # path('products/<int:pk/comments/>', CommentViewSet.as_view()),

    path('test/', index),
 ]