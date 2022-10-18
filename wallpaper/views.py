from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView

from .serializers import CategorySerializer, WallpaperSerializer, CommentSerializer
from .models import Category, Wallpaper, Comment, Like, Rating
from .helpers import OwnerPermission
from .tasks import send_all_user

User = get_user_model()


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


class LikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        wallpaper = get_object_or_404(Wallpaper, id=pk)

        if Like.objects.filter(user=request.user, wallpaper=wallpaper).exists():
            Like.objects.filter(user=request.user, wallpaper=wallpaper).delate()
        else:
            Like.objects.create(user=request.user, wallpaper=wallpaper)
        return Response({'msg': 'Like toggled, 200'})


class RatingAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        value = request.POST.get('value')
        wallpaper = get_object_or_404(Wallpaper, id=pk)

        if not value:
            raise ValueError('value is required')

        if Rating.objects.filter(user=request.user, wallpaper=wallpaper).exists():
            rating = Rating.objects.get(user=request.user, wallpaper=wallpaper)
            rating.value = value
            rating.save()
        else:
            Rating.objects.create(user=request.user, wallpaper=wallpaper, value=value)

        return Response({'msg': 'rating created'}, status=status.HTTP_201_CREATED)

    def delate(self, request, pk):
        wallpaper = get_object_or_404(Wallpaper, id=pk)
        if Rating.objects.get(user=request.user, wallpaper=wallpaper).exists():
            Rating.objects.get(user=request.user, wallpaper=wallpaper).delate()
            return Response({'msg': 'rating delated'})
        else:
            return Response({'msg': 'You didn`t have a rating to remove it'})


def index(request):
    print('hello in view')
    send_all_user.delay()
    return HttpResponse('<h1>Hello</h1>')
