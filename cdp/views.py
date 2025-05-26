from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import (GoldilocksCDP, PrimaryCompanyInfo, SecondaryCompanyInfo, 
                    FinancialInfo, BusinessTracker, UserSearchPrompts, UserHistory)
from .serializers import (  
    GoldilocksCDPSerializer,
    PrimaryCompanyInfoSerializer,
    SecondaryCompanyInfoSerializer,
    FinancialInfoSerializer,
    BusinessTrackerSerializer,
    ExcelUploadSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    UserHistorySerializer,
)
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
import re, requests, json
from .nlp_utils import extract_filters, extract_bracketed_names, extract_summary_json_from_ollama_response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.http import JsonResponse
import chromadb
import time

client = chromadb.Client()
collection = client.get_or_create_collection(name="user_prompts")

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

                """
                Send back the created data as well.
                """
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
    

def build_augmented_prompt(user_query: str) -> str:
    json_instruction = (
        " Please provide a detailed response to the query above. "
        "After your explanation, include a JSON summary of the companies with the following fields: "
        "`name`, `revenue_range`, `ebitda_margin`, and `description`. "
        "The JSON should be placed at the end of the response under a key called 'summary_json'. "
        "Ensure the JSON is valid and clearly separated from the main response."
    )
    return user_query.strip() + json_instruction

class PromptQueryAPIView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt", "")
        filters, limit = extract_filters(prompt['query'])
        queryset = PrimaryCompanyInfo.objects.filter(**filters).distinct()[:limit]

        UserSearchPrompts.objects.create(
            user = request.user,
            prompt = prompt['query'],
            query_filters = prompt['filters']
        )

        # Ollama search
        url = 'http://mmpc.centralus.cloudapp.azure.com:11434/api/generate/'
        headers = {"Content-Type":"application/json"}
        data = {
            "model": "llama3",
            "prompt": build_augmented_prompt(prompt['query']),
            "stream": False
        }

        retry_strategy = Retry(
            total=5,                 # Retry up to 5 times
            backoff_factor=2,        # Exponential backoff: 2s, 4s, 8s...
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("http://", adapter)
        session.mount("https://", adapter)


        try:
            response = session.post(
                url=url,
                headers=headers,
                data=json.dumps(data),
                timeout=300  # Timeout in seconds
            )
            response.raise_for_status()  # Raise error for bad responses
            result = response.json()
            print("Ollama response:", result)

        except requests.exceptions.RequestException as e:
            print("Request failed:", e)

        extracted_companies = extract_summary_json_from_ollama_response(response.text)
        print("Companies list ====> " + str(extracted_companies))
        # json.loads(response.text)['response']

        ollama_company_names = [entry['name'] for entry in extracted_companies[1]['summary_json']]

        in_house_data = PrimaryCompanyInfo.objects.filter(company_name__in=ollama_company_names)

        chroma_db_id = UserSearchPrompts.objects.filter(user=request.user).latest('timestamp').id

        unique_id = f"{request.user.id}_{chroma_db_id}_{int(time.time() * 1000)}"

        add_to_chromadb = collection.add(
            ids= unique_id,
            documents=[prompt["query"]],
            metadatas=[{
                "query_user_id": request.user.id,
                "filters": json.dumps(prompt["filters"])
            }]
        )
        import pdb; pdb.set_trace()
        if len(in_house_data) == 0:
            response_data = {"ollama_data":extracted_companies[0], "orm_data":"No companies were found in the In House Database.", 
                             "fetched_companies":ollama_company_names, "status":200}
        else:
            response_data = {"ollama_data":extracted_companies[0], "orm_data":in_house_data, "fetched_companies":ollama_company_names, "status":200}

        return JsonResponse(response_data)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalidate the refresh token
            request.session.flush()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

"""
Setup Chroma DB, Query API should be processed by NLP, Store filters in UserSearchPrompt Model, Then send query to Ollama, 
once ollama sends resposnse, Store query in ChromaDB, Then send the Ollama response as API response.
"""

class UserHistoryViewSet(viewsets.ReadOnlyModelViewSet):  # ReadOnly to prevent POST/PUT/DELETE
    serializer_class = UserHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserHistory.objects.filter(user=self.request.user).order_by('-timestamp')