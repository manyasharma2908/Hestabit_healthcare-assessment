from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    RegisterSerializer, PatientSerializer, DoctorSerializer, MappingSerializer
)
from .permissions import IsOwnerOrReadOnly

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Only patients created by the authenticated user
        return Patient.objects.filter(created_by=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all().order_by("-created_at")
    serializer_class = DoctorSerializer
    # Read for anyone, write only for authenticated users
    def get_permissions(self):
        if self.request.method in ("GET",):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class MappingViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctorMapping.objects.select_related("patient", "doctor").all().order_by("-created_at")
    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see mappings for patients they own
        return self.queryset.filter(patient__created_by=self.request.user)

class PatientDoctorsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id, created_by=request.user)
        doctors = Doctor.objects.filter(patient_mappings__patient=patient).distinct()
        data = DoctorSerializer(doctors, many=True).data
        return Response(data)
