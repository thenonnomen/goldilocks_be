from rest_framework import serializers
from .models import Employee, Pathway
from django.contrib.auth.models import User
from cdp.serializers import PrimaryCompanyInfoSerializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    past_companies = PrimaryCompanyInfoSerializer(many=True)
    current_company = PrimaryCompanyInfoSerializer()

    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'din', 'designation', 'date_of_appointment',
            'date_of_cessation', 'past_companies', 'current_company'
        ]

class PathwaySerializer(serializers.ModelSerializer):
    target_company = PrimaryCompanyInfoSerializer()

    class Meta:
        model = Pathway
        fields = [
            'id', 'relationship', 'target_company',
            'connection_strength', 'match_score', 'status'
        ]
