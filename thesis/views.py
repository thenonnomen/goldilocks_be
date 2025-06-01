from rest_framework import viewsets
from .models import ThesisLibrary, ThesisQueryResult, ThesisCompanyProfile
from .serializers import ThesisLibrarySerializer, ThesisQueryResultSerializer, ThesisCompanyProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.files.storage import default_storage
from django.conf import settings
import os, re, uuid, pandas as pd

class ExcelUploadView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('file')
        if not excel_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        # Save file temporarily
        temp_file_path = os.path.join(settings.MEDIA_ROOT, f"temp_{uuid.uuid4()}.xlsx")
        with default_storage.open(temp_file_path, 'wb+') as destination:
            for chunk in excel_file.chunks():
                destination.write(chunk)

        # Read Excel with pandas
        try:
            # import pdb; pdb.set_trace()
            df = pd.read_excel(temp_file_path, sheet_name="Thesis AI Watchlist Research")
        except ValueError:
            return Response({"error": "Sheet 'Thesis AI watchlist Research' not found in Excel file."}, status=400)
        except Exception as e:
            return Response({"error": f"Failed to read Excel: {str(e)}"}, status=400)

        success_count = 0
        for _, row in df.iterrows():
            try:
                # Skip rows without company_id or required fields
                # if pd.isna(row.get('Company ID')) or pd.isna(row.get('Country Code')) or pd.isna(row.get('Founded')):
                #     continue

                # Fill missing values with mock data
                def clean(value, default):
                    return default if pd.isna(value) or str(value).strip().upper() == 'N/A' else value

                ceo_first = clean(row.get('First Name - Ceo'), "John")
                ceo_last = clean(row.get('Last Name - Ceo'), "Doe")

                obj = ThesisCompanyProfile.objects.create(
                    company_id=row.get('Company ID'),
                    country_code=row.get('Country Code'),
                    founded = parse_founded(row.get("Founded")),
                    locations=clean(row.get('Locations'), "Unknown"),
                    formatted_locations=clean(row.get('Formatted Locations'), None),
                    employees=clean(row.get('Employees'), None),
                    employee_count=clean(row.get('Employee Count'), None),
                    ceo_name=f"{ceo_first} {ceo_last}",
                    cfo_name="Jane Smith",  # Mock data
                    ceo_rating=clean(row.get('Ceo Rating - Ceo'), "4.2"),
                    total_funding=clean(row.get('Total funding'), "Undisclosed"),
                    latest_funding_round=clean(row.get('Latest funding round'), "Series A"),
                    funding=clean(row.get('Funding'), ""),
                    investors=clean(row.get('Investors'), ""),
                    stock_info=clean(row.get('Stock Info'), ""),
                    organic_social_visits=extract_float(row.get('Organic Social Visits'), 0),
                    paid_search = extract_float(row.get('Paid Search Visits')),
                    mail_visits=extract_float(row.get('Mail Visits')),
                    average_bounce_rate = parse_time_to_minutes(row.get('Average Bounce Rate')),
                    average_time_on_site=parse_time_to_seconds(row.get('Average Time On Site')),
                    organic_search = extract_float(row.get('Organic Search Visits')),
                    traffic_rank = extract_int(row.get('Traffic Rank')),
                    total_users = extract_int(row.get('Total Users')),
                    query_stats={"uploaded_via": "excel_import", "row_index": int(_)},
                )
                # import pdb; pdb.set_trace()
                success_count += 1
            except Exception as e:
                print(e)  # Optionally, collect errors per row

        os.remove(temp_file_path)  # Clean up

        return Response({
            "message": f"Imported {success_count} companies successfully."
        }, status=200)

class ThesisLibraryViewSet(viewsets.ModelViewSet):
    queryset = ThesisLibrary.objects.select_related('findings').all()
    serializer_class = ThesisLibrarySerializer

class ThesisQueryResultViewSet(viewsets.ModelViewSet):
    queryset = ThesisQueryResult.objects.all()
    serializer_class = ThesisQueryResultSerializer

class ThesisCompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = ThesisCompanyProfile.objects.all()
    serializer_class = ThesisCompanyProfileSerializer


def parse_time_to_seconds(value):
    if pd.isna(value):
        return 180  # default
    value = str(value)
    match = re.findall(r'(\d+)', value)
    numbers = list(map(int, match))
    if 'min' in value and 'sec' in value:
        return numbers[0] * 60 + numbers[1]
    elif 'min' in value:
        return numbers[0] * 60
    elif 'sec' in value:
        return numbers[0]
    elif len(numbers) == 2:
        return numbers[0] * 60 + numbers[1]
    elif len(numbers) == 1:
        return numbers[0]
    return 180  # fallback

def clean_founded_date(value):
    try:
        return pd.to_datetime(str(value), errors='raise').date()
    except:
        try:
            # Try extracting 4-digit year
            year_match = re.search(r'\b(19|20)\d{2}\b', str(value))
            if year_match:
                return pd.to_datetime(f"{year_match.group()}-01-01").date()
        except:
            return None
    return None


def extract_float(value, default=0.0):
    try:
        if pd.isna(value):
            return default
        match = re.search(r'\d+(\.\d+)?', str(value))
        return float(match.group()) if match else default
    except:
        return default
    
def extract_int(value, default=0):
    try:
        if pd.isna(value):
            return default
        value = str(value)
        match = re.search(r'\d+', value)
        return int(match.group()) if match else default
    except:
        return default
    
from datetime import datetime

def parse_founded(value):
    try:
        # Try to extract year
        match = re.search(r'\d{4}', str(value))
        if match:
            return datetime.strptime(match.group(), "%Y").date()
    except:
        pass
    return None  # or return a default year

def extract_float(value, default=0.0):
    try:
        if not value:
            return default
        # Match decimal number (like 22.64) anywhere in the string
        match = re.search(r'\d+(\.\d+)?', str(value))
        return float(match.group()) if match else default
    except:
        return default
    
def parse_time_to_minutes(value, default=0.0):
    try:
        if not value:
            return default
        # Extract numbers from string
        # Example: '2.42 min:sec 170' → take '2.42' or convert '2:42' format
        # If time is like 'mm:ss' format e.g. '2:42'
        if ':' in str(value):
            parts = str(value).split(':')
            minutes = float(parts[0])
            seconds = float(parts[1].split()[0])  # remove trailing text
            return minutes + seconds / 60
        else:
            # fallback: extract first float number from string
            match = re.search(r'\d+(\.\d+)?', str(value))
            return float(match.group()) if match else default
    except:
        return default

class ThesisQueryAPIView(APIView):
    def post(self, request):
        query_key_title = request.data.get('query_key')
        company_name = request.data.get('company_name')

        if company_name:
            company_profile = ThesisCompanyProfile.objects.filter(company_name__in = company_name, query_key__contains = query_key_title)
            company_serializer = ThesisCompanyProfileSerializer(company_profile, many=True)
        else:
            company_profiles = ThesisCompanyProfile.objects.filter(query_key__contains=query_key_title)
            company_serializer = ThesisCompanyProfileSerializer(company_profiles, many=True)

        # import pdb; pdb.set_trace()
        # Fetch thesis library and extract query_stats
        query_stats = {}
        thesis_library = ThesisLibrary.objects.filter(
            title=query_key_title
        ).select_related('findings').first()

        if thesis_library and thesis_library.findings and thesis_library.findings.query_stats:
            query_stats = thesis_library.findings.query_stats

        return Response({
            "query_data": company_serializer.data,
            "query_stats": query_stats
        }, status=status.HTTP_200_OK)