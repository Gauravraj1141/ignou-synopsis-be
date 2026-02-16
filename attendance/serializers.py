from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('user_id','username','first_name','last_name','email')

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    role = serializers.ChoiceField(choices=CustomUser.Role.choices, required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email','password','role')

    def validate_email(self, value):
        value = (value or "").strip().lower()
        if not value:
            raise serializers.ValidationError("Email is required.")
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        try:
            with transaction.atomic():
                email = validated_data.get('email', '').strip().lower()
                password = validated_data.pop('password')

                user = CustomUser(
                    username=email,
                    email=email,
                    first_name=validated_data.get('first_name', ''),
                    last_name=validated_data.get('last_name', ''),
                    role=validated_data.get('role')
                )
                user.set_password(password)

                # Run model validation (raises DjangoValidationError on bad data)
                user.full_clean()

                user.save()
                return user
        except IntegrityError:
            raise serializers.ValidationError({"email": "This email is already registered."})
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)


class TokenObtainPairWithRoleSerializer(TokenObtainPairSerializer):
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

class GetUserListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ("user_id", "name", "email", "status", "role", "date_joined")

    def get_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name or getattr(obj, "username", "")

    def get_status(self, obj):
        if hasattr(obj, "get_status_display"):
            return obj.get_status_display()
        return str(getattr(obj, "status", "")).strip().title()

    def get_role(self, obj):
        # Use your CustomUser.Role choices (returns the human-readable label)
        if hasattr(obj, "get_role_display"):
            return obj.get_role_display()
        return str(getattr(obj, "role", "")).strip().title()


class UpdateUserStatusSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    status = serializers.ChoiceField(choices=CustomUser.Status.choices)