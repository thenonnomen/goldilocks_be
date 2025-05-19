from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import GoldilocksCDP, PrimaryCompanyInfo, SecondaryCompanyInfo, FinancialInfo, BusinessTracker, UserSearchPrompts
from .serializers import (  
    GoldilocksCDPSerializer,
    PrimaryCompanyInfoSerializer,
    SecondaryCompanyInfoSerializer,
    FinancialInfoSerializer,
    BusinessTrackerSerializer,
    ExcelUploadSerializer,
)
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re
from .nlp_utils import extract_filters
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import IsAuthenticated


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

class ExcelUploadAPIView(APIView):
    def post(self, request):
        serializer = ExcelUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            try:
                df = pd.read_excel(file)

                for _, row in df.iterrows():
                    print("Primary")
                    try:
                        primary, _ = PrimaryCompanyInfo.objects.update_or_create(
                            company_id=row.get('company_id', 0),
                            defaults={
                                'company_name': row.get('Company Name'),
                                'company_domain': row.get('Company Domain'),
                                'linkedin_company_profile': row.get('LinkedIn Company Profile'),
                                'country_code': row.get('country_code'),
                                'locations': row.get('locations'),
                                'company_size': row.get('company_size'),
                                'organization_type': row.get('organization_type'),
                                'industries': row.get('Industries'),
                                'crunchbase_url': row.get('crunchbase_url'),
                                'founded': row.get('founded'),
                                'headquarters': row.get('headquarters'),
                                'image': row.get('image'),
                                'logo': row.get('logo'),
                                'get_directions_url': row.get('get_directions_url'),
                                'sic_code': row.get('Sic Code'),
                                'name_sectors': row.get('Name - Sectors'),
                                'parent_industry_sectors': row.get('Parent Industry - Sectors'),
                            }
                        )
                    except Exception as e:
                        return Response({"error": str(e)})
                    

                    try:
                        print("secondary")
                        SecondaryCompanyInfo.objects.update_or_create(
                            primary_info=primary,
                            defaults={
                                'employee_count': safe_int(row.get('Employee Count')),
                                'about': row.get('about'),
                                'specialties': row.get('specialties'),
                                'similar': row.get('similar'),
                                'updates': row.get('updates'),
                                'slogan': row.get('slogan'),
                                'affiliated': row.get('affiliated'),
                                'investors': row.get('Investor names'),
                                'parent_website': row.get('Parent Website'),
                                'parent_name': row.get('Parent Name'),
                                'description': row.get('description'),
                            }
                        )
                    except Exception as e:
                        return Response({"error": str(e)})
                    
                    try:
                        print("Financial")
                        # import pdb; pdb.set_trace()
                        FinancialInfo.objects.update_or_create(
                            primary_info=primary,
                            defaults={
                                'employee_count': safe_int(len(row.get('employees'))),
                                'total_funding': clean_funding(row.get('Total funding')),
                                'latest_funding_round': row.get('Latest funding round'),
                                'revenue': row.get('Revenue'),
                                'first_name_ceo': row.get('First Name - Ceo'),
                                'last_name_ceo': row.get('Last Name - Ceo'),
                                'ceo_rating': row.get('Ceo Rating - Ceo'),
                            }
                        )
                    except Exception as e:
                        return Response({"error": str(e)})
                    
                    try:
                        print("Business tracker")
                        BusinessTracker.objects.update_or_create(
                            primary_info=primary,
                            defaults={
                                'organic_social_visits': safe_int(row.get('Organic Social Visits')),
                                'organic_search_visits': safe_int(row.get('Organic Search Visits')),
                                'paid_social_visits': safe_int(row.get('Paid Social Visits')),
                                'paid_search_visits': safe_int(row.get('Paid Search Visits')),
                                'display_ad_visits': safe_int(row.get('Display Ad Visits')),
                                'referral_visits': safe_int(row.get('Referral Visits')),
                                'social_visits': safe_int(row.get('Social Visits')),
                                'search_visits': safe_int(row.get('Search Visits')),
                                'direct_visits': safe_int(row.get('Direct Visits')),
                                'paid_visits': safe_int(row.get('Paid Visits')),
                                'mail_visits': safe_int(row.get('Mail Visits')),
                                'average_pages_per_visit': safe_float(row.get('Average Pages Per Visit')),
                                'average_time_on_site': safe_float(row.get('Average Time On Site')),
                                'average_bounce_rate': safe_float(row.get('Average Bounce Rate')),
                                'traffic_rank': safe_int(row.get('Traffic Rank')),
                                'total_visits': safe_int(row.get('Total Visits')),
                                'total_users': safe_int(row.get('Total Users')),
                                'youtube_link': row.get('Youtube Link'),
                                'twitter_link': row.get('Twitter Link'),
                                'facebook_link': row.get('Facebook Link'),
                                'linkedin_followers': safe_int(row.get('followers')),
                            }
                        )
                    except Exception as e:
                        return Response({"error": str(e)})

                return Response({"message": "Excel data imported successfully."}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def clean_funding(val):
    if not val:
        return 0
    try:
        # Remove commas and non-digit characters
        return int(re.sub(r"[^\d]", "", str(val)))
    except ValueError:
        return 0
    
def safe_int(value, default=0):
    try:
        if pd.isna(value):  # if using pandas
            return default
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

class PromptQueryAPIView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt", "")

        filters, limit = extract_filters(prompt)
        queryset = PrimaryCompanyInfo.objects.filter(**filters).distinct()[:limit]

        UserSearchPrompts.objects.create(
            user = request.user,
            prompt = prompt,
            created_filters = filters
        )
        serializer = PrimaryCompanyInfoSerializer(queryset, many=True)
        return Response(serializer.data)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalidate the refresh token
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)