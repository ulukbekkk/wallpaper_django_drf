from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from .serializers import CategorySerializer, WallpaperSerializer, CommentSerializer, CelerySerializer
from .models import Category, Wallpaper, Comment, Like, Rating
from .helpers import OwnerPermission
from .tasks import send_all_user

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("title of category", openapi.IN_QUERY, "filter wallpapers by category",
                          type=openapi.TYPE_STRING)])
    @action(detail=False, methods=['get'])
    def filter(self, request):
        queryset = self.queryset
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        """ разбиваем queryset на страницы """
        page = self.paginate_queryset(queryset)
        """ сериализуем """
        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("title of wallpaper", openapi.IN_QUERY, "search wallpapers by title",
                          type=openapi.TYPE_STRING)])
    @action(detail=False, methods=['get'])
    def search(self, request):
        queryset = self.get_queryset()
        title = request.query_params.get('title')
        if title:
            queryset = queryset.filter(title_icontains=title)

        serializer = WallpaperSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

    def delete(self, request, pk):
        wallpaper = get_object_or_404(Wallpaper, id=pk)
        if Rating.objects.get(user=request.user, wallpaper=wallpaper).exists():
            Rating.objects.get(user=request.user, wallpaper=wallpaper).delate()
            return Response({'msg': 'rating delated'})
        else:
            return Response({'msg': 'You didn`t have a rating to remove it'})


class CelerySendToEmailAPIView(CreateAPIView):
    serializer_class = CelerySerializer
    # permission_classes = (IsAdminUser,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            send_all_user.delay(request.data.get('text_to'))
            return Response({'msg': 'send to all email'})