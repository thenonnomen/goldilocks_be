from rest_framework import serializers
from .models import GoldilocksCDP, PrimaryCompanyInfo, SecondaryCompanyInfo, FinancialInfo, BusinessTracker

class GoldilocksCDPSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldilocksCDP
        fields = '__all__'

class SecondaryCompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryCompanyInfo
        fields = '__all__'

class FinancialInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialInfo
        fields = '__all__'

class BusinessTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessTracker
        fields = '__all__'

class PrimaryCompanyInfoSerializer(serializers.ModelSerializer):
    secondary_info = SecondaryCompanyInfoSerializer(read_only=True)
    financial_info = FinancialInfoSerializer(read_only=True)
    business_tracker = BusinessTrackerSerializer(read_only=True)

    class Meta:
        model = PrimaryCompanyInfo
        fields = '__all__'
