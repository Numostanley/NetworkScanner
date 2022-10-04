from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication


class AuthProtectedAPIView(APIView):
    """base view for all child views that needs to be authenticated"""
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
