from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=7)
    password2 = serializers.CharField(write_only=True, min_length=7)

    class Meta:
        model = User
        fields = ["last_name", "first_name", "email", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords don't match")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "last_name", "first_name", "email", "role", "is_active", "created_at"]
        read_only_fields = ["id", "is_active", "created_at"]
