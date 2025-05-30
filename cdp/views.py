# Create your views here.
from rest_framework import viewsets
from .models import (GoldilocksCDP, PrimaryCompanyInfo, SecondaryCompanyInfo, 
                    FinancialInfo, BusinessTracker, UserSearchPrompts, UserHistory,
                    WatchlistData, WatchlistInsights)
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
    UserSearchPromptsResultsSerializer
)
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .nlp_utils import extract_filters, extract_bracketed_names, extract_summary_json_from_ollama_response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.http import JsonResponse
from django.db import DatabaseError, IntegrityError
from django.views.decorators.csrf import csrf_exempt
import base64, uuid, chromadb, re, requests, json
from django.shortcuts import render

client = chromadb.Client()
collection = client.get_or_create_collection(name="user_prompts")

class GoldilocksCDPViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on GoldilocksCDP model."""
    queryset = GoldilocksCDP.objects.all()
    serializer_class = GoldilocksCDPSerializer

class PrimaryCompanyInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on PrimaryCompanyInfo model."""
    queryset = PrimaryCompanyInfo.objects.all()
    serializer_class = PrimaryCompanyInfoSerializer

class SecondaryCompanyInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on SecondaryCompanyInfo model."""
    queryset = SecondaryCompanyInfo.objects.all()
    serializer_class = SecondaryCompanyInfoSerializer

class FinancialInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on FinancialInfo model."""
    queryset = FinancialInfo.objects.all()
    serializer_class = FinancialInfoSerializer

class BusinessTrackerViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on BusinessTracker model."""
    queryset = BusinessTracker.objects.all()
    serializer_class = BusinessTrackerSerializer

class ExcelUploadAPIView(APIView):
    """API view for uploading and processing Excel files to import company data."""
    def post(self, request):
        """Handle POST requests for uploading and processing Excel files to import company data."""
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
                    except (DatabaseError, IntegrityError, ValueError, TypeError) as e:
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
                    except (DatabaseError, IntegrityError, ValueError, TypeError) as e:
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
                    except (DatabaseError, IntegrityError, ValueError, TypeError) as e:
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
                    except (DatabaseError, IntegrityError, ValueError, TypeError) as e:
                        return Response({"error": str(e)})

                return Response({"message": "Excel data imported successfully."}, status=status.HTTP_201_CREATED)

            except (DatabaseError, IntegrityError, ValueError, TypeError) as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def clean_funding(val):
    """Clean and convert a funding value to int, removing non-digit characters."""
    if not val:
        return 0
    try:
        # Remove commas and non-digit characters
        return int(re.sub(r"[^\d]", "", str(val)))
    except (DatabaseError, IntegrityError, ValueError, TypeError):
        return 0
    
def safe_int(value, default=0):
    """Safely convert a value to int, returning default if conversion fails or value is NaN."""
    try:
        if pd.isna(value):  # if using pandas
            return default
        return int(value)
    except (DatabaseError, IntegrityError, ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    """Safely convert a value to float, returning default if conversion fails or value is NaN."""
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (DatabaseError, IntegrityError, ValueError, TypeError):
        return default
    

def build_augmented_prompt(user_query: str) -> str:
    """Builds an augmented prompt with instructions for JSON summary extraction."""
    json_instruction = (
        " Please provide a detailed response to the query above. "
        "After your explanation, include a JSON summary of the companies with the following fields: "
        "`name`, `revenue_range`, `ebitda_margin`, and `description`. "
        "The JSON should be placed at the end of the response under a key called 'summary_json'. "
        "Ensure the JSON is valid and clearly separated from the main response."
    )
    return user_query.strip() + json_instruction

class PromptQueryAPIView(APIView):
    """API view for processing user prompts and returning query results."""
    def post(self, request):
        """Handle POST requests for processing user prompts and returning query results."""
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

        unique_id = str(uuid.uuid4())

        query_key = request.data.get("query_key", str(uuid.uuid4()))
        add_to_chromadb = collection.add(
            ids=[query_key],
            documents=[prompt["query"]],
            metadatas=[{
                "query_key": query_key,
                "query_user_id": request.user.id,
                "filters": json.dumps(prompt["filters"]),
                "query_result": ""
            }]
        )
        


        if len(in_house_data) == 0:
            response_data = {
                "ollama_data": extracted_companies[0],
                "orm_data": [],  # Changed to an empty list for consistency
                "fetched_companies": ollama_company_names,
                "status": 200
            }
        else:
            response_data = {
                "ollama_data": extracted_companies[0],
                "orm_data": in_house_data,
                "fetched_companies": ollama_company_names,
                "status": 200
            }

        return JsonResponse(response_data)
    
class LogoutView(APIView):
    """API view to handle user logout and token blacklisting."""
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
    """API view for obtaining JWT token pairs with custom serializer."""
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    """API view for refreshing JWT tokens with custom serializer."""
    serializer_class = CustomTokenRefreshSerializer

class UserHistoryViewSet(viewsets.ReadOnlyModelViewSet):  # ReadOnly to prevent POST/PUT/DELETE
    """ViewSet for retrieving user history records in read-only mode."""
    serializer_class = UserHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return user history records for the authenticated user, ordered by timestamp descending."""
        return UserHistory.objects.filter(user=self.request.user).order_by('-timestamp')

class UserSearchPromptsResultsView(APIView):
    """API view for retrieving user search prompts results."""
    serializer_class = UserSearchPromptsResultsSerializer
    permission_classes = []

    def post(self, request):
        """Handle GET requests for retrieving user search prompts results."""
        query_key = request.data.get("query_key", None)
        query = request.data.get("query", None)
        if query_key is None:
            return Response({"error": "Query key is required"}, status=status.HTTP_400_BAD_REQUEST)
        if query is None:
            return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch companies from WatchlistData with the given query_key
        companies = WatchlistData.objects.filter(query_key__contains=query_key)
        company_list = []
        for company in companies:
            company_list.append({
                "com_name": company.company_name,
                "com_hq": company.headquarters,
                "com_domain": company.company_domain,
                "com_desc": company.about,
                "com_emp": company.employees,
                "com_rev": company.revenue
            })
        # Fetch insights from WatchlistInsights with the given query_key
        insights = WatchlistInsights.objects.filter(query_key=query_key).values_list('insights', flat=True)
        insights_list = list(insights)
        response_data = {
            "query_insight": insights_list,
            "query_data": company_list
        }
        return Response(response_data)

class WatchlistDataExcelUploadAPIView(APIView):
    """API view for uploading and processing Excel files to import WatchlistData."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Handle POST requests for uploading and processing Excel files to import WatchlistData."""
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            df = pd.read_excel(file)
            required_columns = [
                'Company Name', 'Headquarters', 'Company Domain', 'About', 'Employees', 'Revenue'
            ]
            for col in required_columns:
                if col not in df.columns:
                    return Response({"error": f"Missing required column: {col}"}, status=status.HTTP_400_BAD_REQUEST)
            for _, row in df.iterrows():
                WatchlistData.objects.create(
                    company_name=row['Company Name'],
                    headquarters=row['Headquarters'],
                    company_domain=row['Company Domain'],
                    about=row['About'],
                    employees=row['Employees'],
                    revenue=row['Revenue']
                )
            return Response({"message": "WatchlistData imported successfully."}, status=status.HTTP_201_CREATED)
        except (DatabaseError, IntegrityError, ValueError, TypeError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def my_view(request):
    context = {'name': 'Django'}
    return render(request, 'chat.html', context)

@csrf_exempt
def llm_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt')

            models = [
                "mistralai/devstral-small:free",
                "deepseek/deepseek-chat:free",
                "meta-llama/llama-3.3-8b-instruct:free",
                "qwen/qwen3-8b:free"
            ]

            url_encoded = "aHR0cHM6Ly9vcGVucm91dGVyLmFpL2FwaS92MS9jaGF0L2NvbXBsZXRpb25z"
            url = base64.b64decode(url_encoded).decode()

            # API_KEY = "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"
            API_KEY = "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"

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            all_responses = ""

            for model in models:
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                }

                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    model_response = response.json()["choices"][0]["message"]["content"]
                else:
                    model_response = f"Error {response.status_code}: {response.text}"

                all_responses += f"\n🔹 Response from {model}:\n\n{model_response}\n"

            html_bolded_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', all_responses)
            
            # import pdb; pdb.set_trace()

            return JsonResponse({"response": html_bolded_text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)