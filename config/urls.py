from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from health.views import PatientViewSet, DoctorViewSet, MappingViewSet, RegisterView, PatientDoctorsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router =DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patient")
router.register(r"doctors", DoctorViewSet, basename="doctor")
router.register(r"mappings", MappingViewSet, basename="mapping")

urlpatterns = [
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/", include(router.urls)),
    path("api/mappings/<int:patient_id>/", PatientDoctorsView.as_view(), name="patient-doctors"),
]
