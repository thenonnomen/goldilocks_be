from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Employee, Pathway
from .serializers import EmployeeSerializer, PathwaySerializer
from rest_framework import status, viewsets

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('user', 'current_company').prefetch_related('past_companies')
    serializer_class = EmployeeSerializer
    lookup_field = 'id'

class PathwayViewSet(viewsets.ModelViewSet):
    queryset = Pathway.objects.select_related('target_company')
    serializer_class = PathwaySerializer
    lookup_field = 'id'