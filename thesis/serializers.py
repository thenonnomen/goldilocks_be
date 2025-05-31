from rest_framework import serializers
from .models import ThesisLibrary, ThesisQueryResult, ThesisCompanyProfile

class ThesisQueryResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThesisQueryResult
        fields = ['id', 'query', 'query_id', 'created_at', 'query_stats']

class ThesisLibrarySerializer(serializers.ModelSerializer):
    findings = ThesisQueryResultSerializer(read_only=True)
    findings_id = serializers.PrimaryKeyRelatedField(
        queryset=ThesisQueryResult.objects.all(), source='findings', write_only=True
    )

    class Meta:
        model = ThesisLibrary
        fields = [
            'id', 'title', 'description', 'finding_summary',
            'findings', 'findings_id', 'created_at'
        ]

class ThesisCompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThesisCompanyProfile
        fields = '__all__'