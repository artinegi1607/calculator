from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers, views
from rest_framework.response import Response


@receiver(post_save, sender=User)
def create_auth_token(user, **kwargs):
    token = Token.objects.get_or_create(user=user)
    return token


class ObtainToken(views.APIView):

    def post(self, request, *args, **kwargs):
        if request.data:
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = create_auth_token(user)
                return Response({
                    'token': token.serializable_value('key'),
                    "username": username})
