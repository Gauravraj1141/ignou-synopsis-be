from django.forms import ValidationError
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import  UserSerializer, RegisterSerializer, GetUserListSerializer, UpdateUserStatusSerializer
from .models import CustomUser, FaceEmbedding, Attendance
from django.utils import timezone
from datetime import date
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenObtainPairWithRoleSerializer
from .permissions import IsAdminRole
import face_recognition
import numpy as np
import cv2
from rest_framework.parsers import MultiPartParser
import numpy as np
from scipy.spatial.distance import euclidean


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
    

class RegisterFaceAPIView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        image_files = request.FILES.getlist('image')
        user_id = request.data.get("user_id")

        if not image_files:
            return Response({"error": "No image provided"}, status=400)

        saved_image = 0
        for image_file in image_files:
            image = face_recognition.load_image_file(image_file)
            encodings = face_recognition.face_encodings(image)
            print(encodings,"it is encodings")

            if not encodings:
                continue

            embedding = encodings[0].tolist()

            FaceEmbedding.objects.create(
                user_id=user_id,
                embedding_data=embedding
            )
            saved_image +=1


        if saved_image == 0:
            return Response({"error": "No face detected"}, status=400)
        
        CustomUser.objects.filter(user_id=user_id).update(is_registered=True)
        return Response({"message": "Face registered successfully"})
    


class MarkAttendanceApiView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        image_file = request.FILES.get('image')
        user_id = request.user.user_id

        Attendance_marked = Attendance.objects.filter(user_id=user_id, date=date.today()).exists()
        if Attendance_marked:
            return Response({"error": "Attendance has already been marked today."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not image_file:
            return Response({"error": "No image provided"}, status=400)
        
        image = face_recognition.load_image_file(image_file)
        embeddings =  face_recognition.face_encodings(image)
        if len(embeddings)==0:
            return Response({"error": "No face detected in the image. Please try again."}, status=400)
        
        new_embedding = embeddings[0]

        stored_embeddings = FaceEmbedding.objects.filter(user_id=user_id)
        for emb in stored_embeddings:
            stored = np.array(emb.embedding_data)
            distance = euclidean(new_embedding, stored)

            if distance < 0.6:
                Attendance.objects.create(
                    user_id=user_id,
                    date = date.today()
                )
                return Response({"message": "Attandance Marked successfully"})
            
        return Response({"error": "Face verification failed. Please ensure you are the registered user."}, status=400)
            