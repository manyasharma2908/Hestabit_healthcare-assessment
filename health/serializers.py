from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Patient, Doctor, PatientDoctorMapping

class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "username", "password")
        extra_kwargs = {"email": {"required": True}}

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        name = validated_data.pop("name")
        email = validated_data.pop("email")
        username = validated_data.get("username") or email
        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data.pop("password"),
        )
        # split name if possible
        parts = [p for p in name.strip().split(" ") if p]
        if parts:
            user.first_name = parts[0]
            user.last_name = " ".join(parts[1:])
            user.save()
        return user

class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.id")

    class Meta:
        model = Patient
        fields = ("id", "name", "age", "gender", "address", "created_by", "created_at", "updated_at")

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ("id", "name", "specialization", "email", "phone", "created_at", "updated_at")

class MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ("id", "patient", "doctor", "created_at")

    def validate(self, attrs):
        # prevent mapping if patient does not belong to the requesting user
        request = self.context.get("request")
        patient = attrs.get("patient")
        if request and patient and patient.created_by != request.user:
            raise serializers.ValidationError("You can only assign doctors to your own patients.")
        return attrs
