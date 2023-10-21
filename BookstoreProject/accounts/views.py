from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


@api_view(["POST"])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = get_object_or_404(CustomUser,email=email)
    if user and user.check_password(password):
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token":token.key},status=status.HTTP_200_OK)
    return Response({"error":"Invalid Credentials!"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        # deleting user's token
        request.user.auth_token.delete()
        return Response({"message":"User successfully loged out!"},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":e},status=status.HTTP_500_INTERNAL_SERVER_ERROR)