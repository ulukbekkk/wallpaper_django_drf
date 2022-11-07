from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Wallpaper, Comment

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)


class FilterCommentListSerializer(serializers.ListSerializer):
    # Фильтрация children, чтобы не выходили на одном уровне parent
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ChildrenSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = CommentForProductSerializer(instance, context=self.context)
        return serializer.data


class CommentForProductSerializer(serializers.ModelSerializer):
    children = ChildrenSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        exclude = ('created_at',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.email
        return rep


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'body', 'wallpaper', 'parent')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.email
        return rep

    def create(self, validate_data):
        request = self.context.get('request')
        print(request)
        comment = Comment.objects.create(user=request.user, **validate_data)
        return comment


class WallpaperSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    comment = CommentForProductSerializer(many=True, read_only=True)

    class Meta:
        model = Wallpaper
        fields = ('id', 'image', 'title', 'created_at', 'category', 'comment',)

    def create(self, validated_data):
        request = self.context.get('request')
        wallpaper = Wallpaper.objects.create(user=request.user, **validated_data)
        return wallpaper

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.email
        rep['like'] = instance.like.all().count()
        print(dir(instance.like.all()))
        rep['rating'] = instance.rating.aggregate(Avg('value'))
        return rep


class CelerySerializer(serializers.Serializer):
    text_to = serializers.CharField(write_only=True, max_length=500,)
