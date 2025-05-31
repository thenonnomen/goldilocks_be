"""
URL configuration for goldy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# imports for Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from cdp.views import ExcelUploadAPIView, PromptQueryAPIView, LogoutView, CustomTokenObtainPairView, CustomTokenRefreshView, my_view, llm_chat
from cdp.views import (UserSearchPromptsResultsView, ExcelUploadAPIView, PromptQueryAPIView, LogoutView, 
                        CustomTokenObtainPairView, CustomTokenRefreshView, WatchlistDataExcelUploadAPIView)
from thesis.views import upload_excel

schema_view = get_schema_view(
   openapi.Info(
      title="Goldilocks",
      default_version='v1',
      description="Golilocks CDP API's",
    #   terms_of_service="https://www.google.com/policies/terms/",
    #   contact=openapi.Contact(email="contact@yourapi.local"),
    #   license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),    
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('demo/', include("cdp.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('upload-excel/', ExcelUploadAPIView.as_view(), name='upload-excel'),
    path("query/", PromptQueryAPIView.as_view(), name="prompt-query"),
    path('chat', my_view, name='home'),
    path('llm-chat/', llm_chat, name='llm_chat'),
    path('emp/', include("handshake.urls")),
    path('thesis/', include("thesis.urls")),
    path('demo/prompt_results', UserSearchPromptsResultsView.as_view(), name='prompt_results'),
    path('upload-watchlist-excel/', WatchlistDataExcelUploadAPIView.as_view(), name='upload-watchlist-excel'),
    path("upload-excel2/", upload_excel, name="upload-excel"),
]
