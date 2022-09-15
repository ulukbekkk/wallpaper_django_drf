from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import index, WallpaperModelViewSet, CategoryModelViewSet, CommentViewSet

router = DefaultRouter()
router.register('products', WallpaperModelViewSet)
router.register('categories', CategoryModelViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('products/<int:pk/comments/>', CommentViewSet.as_view()),

    path('test/', index),
 ]