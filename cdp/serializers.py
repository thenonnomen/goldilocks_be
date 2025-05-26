from rest_framework import serializers
from .models import GoldilocksCDP, PrimaryCompanyInfo, SecondaryCompanyInfo, FinancialInfo, BusinessTracker
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings

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

class ExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    country = serializers.CharField(required=False)
    region = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)

    def validate(self, attrs):
        data = super().validate(attrs)

        # Access user
        user = self.user

        # Extract extra fields
        country = self.initial_data.get("country")
        region = self.initial_data.get("region")
        currency = self.initial_data.get("currency")

        # Optionally: store in session
        request = self.context.get('request')
        if request:
            request.session['country'] = country
            request.session['region'] = region
            request.session['currency'] = currency

        # Include in response
        data.update({
            "country": country,
            "region": region,
            "currency": currency,
            "user_id": user.id,
            "username": user.username,
        })
        # Extend the session to DB and store it in db to display in admin panel.

        return data
    
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        request = self.context.get('request')

        if request and hasattr(request, 'session'):
            data['country'] = request.session.get('country')
            data['region'] = request.session.get('region')
            data['currency'] = request.session.get('currency')

        return data