from django.shortcuts import render, HttpResponse, get_object_or_404
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from .serializers import CategorySerializer, WallpaperSerializer, CommentSerializer
from .models import Category, Wallpaper, Comment, Like
from .helpers import OwnerPermission


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = (IsAdminUser,)


class WallpaperModelViewSet(ModelViewSet):
    queryset = Wallpaper.objects.all()
    serializer_class = WallpaperSerializer

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_context(self):
        return {'request': self.request}


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, OwnerPermission)

    def get_serializer_context(self):
        return {'request': self.request}


class Like(APIView):
    def get(self, request, pk):
        wallpaper = get_object_or_404(Wallpaper, id=pk)

        if Like.objects.filter(user=request.user, wallpaper=wallpaper).exists():
            Like.objects.filter(user=request.user, wallpaper=wallpaper).delate()
        else:
            Like.objects.create(user=request.user, wallpaper=wallpaper)
        return Response({'msg': 'Like toggled, 200'})


def index(request):
    return HttpResponse('<h1>Hello</h1>')
