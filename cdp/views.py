from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import GoldilocksCDP, PrimaryCompanyInfo, SecondaryCompanyInfo, FinancialInfo, BusinessTracker
from .serializers import (  
    GoldilocksCDPSerializer,
    PrimaryCompanyInfoSerializer,
    SecondaryCompanyInfoSerializer,
    FinancialInfoSerializer,
    BusinessTrackerSerializer,
)

class GoldilocksCDPViewSet(viewsets.ModelViewSet):
    queryset = GoldilocksCDP.objects.all()
    serializer_class = GoldilocksCDPSerializer

class PrimaryCompanyInfoViewSet(viewsets.ModelViewSet):
    queryset = PrimaryCompanyInfo.objects.all()
    serializer_class = PrimaryCompanyInfoSerializer

class SecondaryCompanyInfoViewSet(viewsets.ModelViewSet):
    queryset = SecondaryCompanyInfo.objects.all()
    serializer_class = SecondaryCompanyInfoSerializer

class FinancialInfoViewSet(viewsets.ModelViewSet):
    queryset = FinancialInfo.objects.all()
    serializer_class = FinancialInfoSerializer

class BusinessTrackerViewSet(viewsets.ModelViewSet):
    queryset = BusinessTracker.objects.all()
    serializer_class = BusinessTrackerSerializer