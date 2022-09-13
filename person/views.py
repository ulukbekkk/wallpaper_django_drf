from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from decouple import config

from .serializers import *

User = get_user_model()


class RegisterAPIView(APIView):

    def post(self, request):
        serializers = RegisterSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response('Account created', status=201)


class LogOutAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({'status': 'OK, goodbye, all refresh tokens blacklisted'})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": 'Ok, goodbye'})


@api_view(['GET'])
def activate(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True
    user.activation_code = ''
    user.save()
    return redirect(config('DOMAIN'))
