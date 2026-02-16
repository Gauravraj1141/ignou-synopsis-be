from django.forms import ValidationError
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import  UserSerializer, RegisterSerializer, GetUserListSerializer, UpdateUserStatusSerializer
from .models import CustomUser
from django.utils import timezone
from datetime import date
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenObtainPairWithRoleSerializer
from .permissions import IsAdminRole

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(APIView):
    # permission_classes = [IsAdminRole]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class TokenObtainPairWithRoleView(TokenObtainPairView):
    serializer_class = TokenObtainPairWithRoleSerializer

# admin apis
class GetUserList(generics.ListAPIView):
    serializer_class = GetUserListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-date_joined')




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UpdateUserStatusAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request):
        serializer = UpdateUserStatusSerializer(data=request.data)

        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]
            new_status = serializer.validated_data["status"]

            try:
                user = CustomUser.objects.get(user_id=user_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            user.status = new_status
            user.save()

            return Response(
                {"message": "Status updated successfully"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)