from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('user_id','username','first_name','last_name','email')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email','password','role')

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data.get('email',''),
            email=validated_data.get('email',''),
            first_name=validated_data.get('first_name',''),
            last_name=validated_data.get('last_name',''),
            role = validated_data.get('role','')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TokenObtainPairWithRoleSerializer(TokenObtainPairSerializer):
    # Optional extra login parameter.
    # If provided, we validate it matches the account's real role (do not trust client input).
    role = serializers.ChoiceField(choices=CustomUser.Role.choices, required=False)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

    def validate(self, attrs):
        requested_role = attrs.get('role')
        data = super().validate(attrs)

        if requested_role and requested_role != self.user.role:
            raise serializers.ValidationError({'role': 'Role does not match this account.'})

        data['role'] = self.user.role
        data['user_id'] = str(getattr(self.user, 'user_id', self.user.pk))
        return data

# class FaceEmbeddingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FaceEmbedding
#         fields = ('id','user','embedding','created_at')

# class AttendanceSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = Attendance
#         fields = ('id','user','date','status','timestamp')

class GetUserListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ("user_id", "name", "email", "status", "role")

    def get_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name or getattr(obj, "username", "")

    def get_status(self, obj):
        # Common Django user flag; adjust if your model has a dedicated `status` field
        if hasattr(obj, "is_active"):
            return "active" if obj.is_active else "inactive"
        return getattr(obj, "status", None)