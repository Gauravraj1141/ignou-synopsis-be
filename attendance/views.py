from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import  UserSerializer, RegisterSerializer, GetUserListSerializer
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


# class MarkAttendanceView(APIView):
#     """
#     Placeholder endpoint for marking attendance via face recognition.
#     Expected payload: { "embedding": [float,...] }
#     Real face-matching logic to be implemented: compare incoming embedding with stored embeddings
#     """
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         today = date.today()
#         attendance, created = Attendance.objects.get_or_create(user=user, date=today)
#         attendance.status = 'present'
#         attendance.save()
#         return Response({'status': 'marked', 'date': str(today)})

# class AttendanceReportView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = AttendanceSerializer

#     def get_queryset(self):
#         # For admins return all, else filter by user
#         user = self.request.user
#         if user.is_staff:
#             return Attendance.objects.all().order_by('-date')
#         return Attendance.objects.filter(user=user).order_by('-date')
